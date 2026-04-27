from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed dummy users for testing'

    def handle(self, *args, **kwargs):
        # Tạo Admin (không cần xóa toàn bộ User để tránh lỗi)
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@shopx.com', '123456', user_type='admin', name='Quản trị viên')
            
        # Tạo Staff
        if not User.objects.filter(username='staff1').exists():
            User.objects.create_user(username='staff1', password='123456', user_type='staff', role='Sale', name='Nhân viên Bán hàng')
        if not User.objects.filter(username='staff2').exists():
            User.objects.create_user(username='staff2', password='123456', user_type='staff', role='Support', name='Nhân viên CSKH')
            
        # Tạo Customer
        if not User.objects.filter(username='customer1@shopx.com').exists():
            User.objects.create_user(username='customer1@shopx.com', email='customer1@shopx.com', password='123456', user_type='customer', name='Nguyễn Văn Khách')
        if not User.objects.filter(username='customer2@shopx.com').exists():
            User.objects.create_user(username='customer2@shopx.com', email='customer2@shopx.com', password='123456', user_type='customer', name='Trần Thị Mua')
            
        self.stdout.write(self.style.SUCCESS('Tạo thành công các tài khoản Test (Mật khẩu: 123456)'))
