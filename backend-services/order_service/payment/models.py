from django.db import models
from django.utils import timezone
from orders.models import Order

class Payment(models.Model):
    order = models.OneToOneField(Order, related_name='payment', on_delete=models.CASCADE)
    method = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, default="Pending")
    amount = models.FloatField(null=True)
    paid_at = models.DateTimeField(null=True)
    transaction_id = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'payment'

class Refund(models.Model):
    order = models.ForeignKey(Order, related_name='refunds', on_delete=models.CASCADE)
    amount = models.FloatField()
    reason = models.TextField(null=True)
    status = models.CharField(max_length=255, default="REQUESTED")
    requested_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'refund'
