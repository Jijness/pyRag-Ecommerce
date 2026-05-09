from django.db import models
from django.utils import timezone


class GiftCard(models.Model):
    """
    Entity — GiftCard (chuyển từ interaction_service).
    """
    code = models.CharField(max_length=50, unique=True, db_index=True)
    amount = models.FloatField()               # Mệnh giá gốc
    remaining_amount = models.FloatField()     # Số tiền còn lại
    issued_to = models.IntegerField(null=True, blank=True)  # Soft ref → Customer
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'gift_card'

    def __str__(self):
        return f"GiftCard({self.code}, remaining={self.remaining_amount})"
