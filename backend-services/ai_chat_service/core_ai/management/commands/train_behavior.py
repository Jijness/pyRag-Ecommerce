from django.core.management.base import BaseCommand
from django.conf import settings
from core_ai.behavior_model import BehaviorModel
import os

class Command(BaseCommand):
    help = 'Triggers the training process for the Deep Learning Behavior Models.'

    def handle(self, *args, **options):
        self.stdout.write("Khởi động huấn luyện Deep Learning...")
        model = BehaviorModel(settings.BASE_DIR)
        
        # Bắt buộc train lại
        model.train_and_save()
        
        self.stdout.write(self.style.SUCCESS("Hoàn thành huấn luyện mô hình!"))
        self.stdout.write(f"Dữ liệu và biểu đồ được lưu tại: {os.path.join(settings.BASE_DIR, 'plots')}")
