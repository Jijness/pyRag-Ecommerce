from django.db import models
from django.utils import timezone


class Cart(models.Model):
    """
    Aggregate Root — Cart Context.
    Lưu giỏ hàng của Customer hoặc Guest (qua session_id).
    """
    customer_id = models.IntegerField(null=True, blank=True, db_index=True)
    session_id = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart'
        indexes = [
            models.Index(fields=['customer_id', 'is_active']),
        ]

    def __str__(self):
        return f"Cart(id={self.pk}, customer={self.customer_id}, active={self.is_active})"


class CartItem(models.Model):
    """
    Entity — thuộc Cart Aggregate.
    Không lưu price — giá lấy real-time từ Product Service khi cần.
    """
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product_id = models.IntegerField(db_index=True)  # Soft ref → Product Context
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'cart_item'
        unique_together = ('cart', 'product_id')  # mỗi product 1 dòng trong 1 giỏ

    def __str__(self):
        return f"CartItem(cart={self.cart_id}, product={self.product_id}, qty={self.quantity})"
