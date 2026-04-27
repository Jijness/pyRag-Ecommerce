from django.db import models
from django.utils import timezone

class Order(models.Model):
    customer_id = models.IntegerField()
    staff_id = models.IntegerField(null=True)
    coupon_code = models.CharField(max_length=255, null=True)
    total_price = models.FloatField()
    total_quantity = models.IntegerField()
    status = models.CharField(max_length=255, default="PENDING")
    date = models.DateTimeField(default=timezone.now)
    note = models.TextField(null=True)
    
    saga_status = models.CharField(max_length=255, default="INITIATED")
    saga_step = models.CharField(max_length=255, null=True)
    saga_error = models.TextField(null=True)

    class Meta:
        db_table = 'order'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book_id = models.IntegerField()
    book_title = models.CharField(max_length=255, null=True)
    price = models.FloatField()
    quantity = models.IntegerField()

    class Meta:
        db_table = 'order_item'
