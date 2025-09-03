from django.contrib import admin
from .models import Category, Transaction, Budget

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'color', 'icon']
    list_filter = ['type']
    search_fields = ['name']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount', 'description', 'date', 'created_at']
    list_filter = ['category__type', 'date', 'created_at']
    search_fields = ['description', 'user__username']
    date_hierarchy = 'date'

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount', 'month', 'created_at']
    list_filter = ['month', 'category__type']
    search_fields = ['user__username', 'category__name']
    date_hierarchy = 'month'
