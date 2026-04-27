from django.db import models
from orders.models import Order

class Shipping(models.Model):
    order = models.OneToOneField(Order, related_name='shipping', on_delete=models.CASCADE)
    method = models.CharField(max_length=255, null=True)
    fee = models.FloatField(default=0)
    tracking_number = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, default="PENDING")
    shipped_at = models.DateTimeField(null=True)
    delivered_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'shipping'
