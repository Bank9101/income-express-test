from django.core.management.base import BaseCommand
from webpage.models import Category

class Command(BaseCommand):
    help = 'สร้างหมวดหมู่เริ่มต้นสำหรับรายรับ-รายจ่าย'

    def handle(self, *args, **options):
        # หมวดหมู่รายรับ
        income_categories = [
            {'name': 'เงินเดือน', 'type': 'income', 'color': '#28a745', 'icon': 'fas fa-money-bill-wave'},
            {'name': 'โบนัส', 'type': 'income', 'color': '#20c997', 'icon': 'fas fa-gift'},
            {'name': 'รายได้เสริม', 'type': 'income', 'color': '#17a2b8', 'icon': 'fas fa-briefcase'},
            {'name': 'ดอกเบี้ย', 'type': 'income', 'color': '#6f42c1', 'icon': 'fas fa-percentage'},
            {'name': 'อื่นๆ', 'type': 'income', 'color': '#fd7e14', 'icon': 'fas fa-plus-circle'},
        ]

        # หมวดหมู่รายจ่าย
        expense_categories = [
            {'name': 'อาหาร', 'type': 'expense', 'color': '#dc3545', 'icon': 'fas fa-utensils'},
            {'name': 'การเดินทาง', 'type': 'expense', 'color': '#fd7e14', 'icon': 'fas fa-car'},
            {'name': 'ที่พัก', 'type': 'expense', 'color': '#6f42c1', 'icon': 'fas fa-home'},
            {'name': 'เสื้อผ้า', 'type': 'expense', 'color': '#e83e8c', 'icon': 'fas fa-tshirt'},
            {'name': 'ความบันเทิง', 'type': 'expense', 'color': '#ffc107', 'icon': 'fas fa-gamepad'},
            {'name': 'สุขภาพ', 'type': 'expense', 'color': '#28a745', 'icon': 'fas fa-heartbeat'},
            {'name': 'การศึกษา', 'type': 'expense', 'color': '#17a2b8', 'icon': 'fas fa-graduation-cap'},
            {'name': 'ช้อปปิ้ง', 'type': 'expense', 'color': '#6c757d', 'icon': 'fas fa-shopping-cart'},
            {'name': 'อื่นๆ', 'type': 'expense', 'color': '#495057', 'icon': 'fas fa-ellipsis-h'},
        ]

        # สร้างหมวดหมู่รายรับ
        for cat_data in income_categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'สร้างหมวดหมู่รายรับ: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'หมวดหมู่รายรับมีอยู่แล้ว: {category.name}')
                )

        # สร้างหมวดหมู่รายจ่าย
        for cat_data in expense_categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'สร้างหมวดหมู่รายจ่าย: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'หมวดหมู่รายจ่ายมีอยู่แล้ว: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('สร้างหมวดหมู่เริ่มต้นเสร็จสิ้น!')
        )
