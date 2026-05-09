from django.db import models
from django.utils import timezone


class Payment(models.Model):
    """
    Aggregate Root — Payment Context.
    Snapshot amount từ Order tại thời điểm tạo.
    order_id là Soft Reference — không dùng FK vật lý xuyên service.
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'
        COD_PAID = 'COD_PAID', 'COD Paid'
        REFUNDED = 'REFUNDED', 'Refunded'

    class MethodType(models.TextChoices):
        ONLINE = 'online', 'Online'
        COD = 'cod', 'Cash on Delivery'
        GIFT_CARD = 'gift_card', 'Gift Card'

    order_id = models.IntegerField(unique=True, db_index=True)   # Soft ref → Order
    customer_id = models.IntegerField(db_index=True)              # Soft ref → User
    amount = models.FloatField()
    currency = models.CharField(max_length=10, default='VND')
    method_type = models.CharField(max_length=20, choices=MethodType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    gateway_ref = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'payment'

    def __str__(self):
        return f"Payment(order={self.order_id}, method={self.method_type}, status={self.status})"


class TransactionLog(models.Model):
    """
    Entity trong Payment Aggregate.
    Audit trail mọi sự kiện liên quan đến Payment.
    """
    class EventType(models.TextChoices):
        INITIATED = 'INITIATED'
        CONFIRMED = 'CONFIRMED'
        FAILED = 'FAILED'
        REFUNDED = 'REFUNDED'

    payment = models.ForeignKey(Payment, related_name='transaction_logs', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=20, choices=EventType.choices)
    gateway_transaction_id = models.CharField(max_length=255, null=True, blank=True)
    response_code = models.CharField(max_length=50, null=True, blank=True)
    response_message = models.TextField(null=True, blank=True)
    logged_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'transaction_log'
        ordering = ['logged_at']


class Refund(models.Model):
    """Entity trong Payment Aggregate."""
    class Status(models.TextChoices):
        REQUESTED = 'REQUESTED'
        APPROVED = 'APPROVED'
        COMPLETED = 'COMPLETED'
        REJECTED = 'REJECTED'

    payment = models.OneToOneField(Payment, related_name='refund', on_delete=models.CASCADE)
    order_id = models.IntegerField(db_index=True)  # Soft ref
    amount = models.FloatField()
    reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED)
    requested_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.IntegerField(null=True, blank=True)  # Soft ref → Admin User

    class Meta:
        db_table = 'refund'
