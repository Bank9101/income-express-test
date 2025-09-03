from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Transaction, Category, Budget
from .forms import TransactionForm, CategoryForm, BudgetForm, UserRegistrationForm
import calendar

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'ลงทะเบียนสำเร็จ!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'เข้าสู่ระบบสำเร็จ!')
            return redirect('dashboard')
        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'ออกจากระบบสำเร็จ!')
    return redirect('index')

@login_required
def dashboard(request):
    try:
        # Get current month data
        now = timezone.now()
        current_month = now.replace(day=1)
        
        # Get transactions for current month
        transactions = Transaction.objects.filter(
            user=request.user,
            date__gte=current_month,
            date__lt=current_month.replace(day=1) + timedelta(days=32)
        ).order_by('-date')
        
        # Calculate totals
        total_income = transactions.filter(category__type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = transactions.filter(category__type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        balance = total_income - total_expense
        
        # Get recent transactions
        recent_transactions = transactions[:10]
        
        # Get categories for quick add
        categories = Category.objects.all()
        
    except Exception as e:
        # Handle database errors (e.g., missing tables)
        messages.error(request, f'Database error: {str(e)}. Please check your database configuration.')
        total_income = 0
        total_expense = 0
        balance = 0
        recent_transactions = []
        categories = []
        current_month = now
    
    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'recent_transactions': recent_transactions,
        'categories': categories,
        'current_month': current_month.strftime('%B %Y'),
    }
    return render(request, 'dashboard.html', context)

@login_required
def transactions(request):
    try:
        transactions_list = Transaction.objects.filter(user=request.user).order_by('-date')
        
        # Filter by type
        transaction_type = request.GET.get('type')
        if transaction_type:
            transactions_list = transactions_list.filter(category__type=transaction_type)
        
        # Filter by date range
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date:
            transactions_list = transactions_list.filter(date__gte=start_date)
        if end_date:
            transactions_list = transactions_list.filter(date__lte=end_date)
            
    except Exception as e:
        messages.error(request, f'Database error: {str(e)}. Please check your database configuration.')
        transactions_list = []
        transaction_type = None
        start_date = None
        end_date = None
    
    context = {
        'transactions': transactions_list,
        'transaction_type': transaction_type,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'transactions.html', context)

@login_required
def add_transaction(request):
    try:
        if request.method == 'POST':
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                messages.success(request, 'เพิ่มรายการสำเร็จ!')
                return redirect('transactions')
        else:
            form = TransactionForm()
            
    except Exception as e:
        messages.error(request, f'Database error: {str(e)}. Please check your database configuration.')
        form = TransactionForm()
    
    context = {
        'form': form,
        'title': 'เพิ่มรายการใหม่'
    }
    return render(request, 'transaction_form.html', context)

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขรายการสำเร็จ!')
            return redirect('transactions')
    else:
        form = TransactionForm(instance=transaction)
    
    context = {
        'form': form,
        'title': 'แก้ไขรายการ',
        'transaction': transaction
    }
    return render(request, 'transaction_form.html', context)

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'ลบรายการสำเร็จ!')
        return redirect('transactions')
    return render(request, 'delete_confirm.html', {'transaction': transaction})

@login_required
def categories(request):
    try:
        categories_list = Category.objects.all()
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'เพิ่มหมวดหมู่สำเร็จ!')
                return redirect('categories')
        else:
            form = CategoryForm()
            
    except Exception as e:
        messages.error(request, f'Database error: {str(e)}. Please check your database configuration.')
        categories_list = []
        form = CategoryForm()
    
    context = {
        'categories': categories_list,
        'form': form
    }
    return render(request, 'categories.html', context)

@login_required
def budgets(request):
    budgets_list = Budget.objects.filter(user=request.user).order_by('-month')
    
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'เพิ่มงบประมาณสำเร็จ!')
            return redirect('budgets')
    else:
        form = BudgetForm()
    
    context = {
        'budgets': budgets_list,
        'form': form
    }
    return render(request, 'budgets.html', context)

@login_required
def reports(request):
    # Get date range
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    if request.GET.get('start_date'):
        start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d').date()
    if request.GET.get('end_date'):
        end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d').date()
    
    # Get transactions in date range
    transactions = Transaction.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=end_date
    )
    
    # Calculate totals by category
    income_by_category = transactions.filter(category__type='income').values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    expense_by_category = transactions.filter(category__type='expense').values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    # Monthly trend (last 6 months)
    monthly_data = []
    for i in range(6):
        month_start = end_date.replace(day=1) - timedelta(days=30*i)
        month_end = month_start.replace(day=28) + timedelta(days=4)
        month_end = month_end.replace(day=1) - timedelta(days=1)
        
        month_transactions = transactions.filter(
            date__gte=month_start,
            date__lte=month_end
        )
        
        month_income = month_transactions.filter(category__type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        month_expense = month_transactions.filter(category__type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        
        monthly_data.append({
            'month': month_start.strftime('%B %Y'),
            'income': month_income,
            'expense': month_expense,
            'balance': month_income - month_expense
        })
    
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'income_by_category': income_by_category,
        'expense_by_category': expense_by_category,
        'monthly_data': monthly_data,
        'total_income': sum(item['income'] for item in monthly_data),
        'total_expense': sum(item['expense'] for item in monthly_data),
    }
    return render(request, 'reports.html', context)
