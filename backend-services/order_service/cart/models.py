from django.db import models
from django.utils import timezone

class Cart(models.Model):
    customer_id = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'cart'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    book_id = models.IntegerField()
    quantity = models.IntegerField(default=1)
    unit_price = models.FloatField(null=True)

    class Meta:
        db_table = 'cart_item'
