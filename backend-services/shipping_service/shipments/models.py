from django.db import models
from django.utils import timezone
from couriers.models import Courier


class Shipment(models.Model):
    """
    Aggregate Root — Shipping Context.
    """
    class Status(models.TextChoices):
        AWAITING_PAYMENT = 'AWAITING_PAYMENT'  # Đang chờ thanh toán (nếu là online)
        PROCESSING = 'PROCESSING'            # Đã thanh toán hoặc COD, đang chuẩn bị hàng
        SHIPPING = 'SHIPPING'                # Đang giao
        DELIVERED = 'DELIVERED'              # Giao thành công
        FAILED = 'FAILED'                    # Giao thất bại

    order_id = models.IntegerField(unique=True, db_index=True)  # Soft ref
    customer_id = models.IntegerField(db_index=True)            # Soft ref
    shipping_address = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PROCESSING)
    courier = models.ForeignKey(Courier, null=True, blank=True, on_delete=models.SET_NULL, related_name='shipments')
    tracking_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    shipping_fee = models.FloatField(default=0.0)
    created_at = models.DateTimeField(default=timezone.now)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'shipment'

    def __str__(self):
        return f"Shipment(order={self.order_id}, status={self.status})"


class ShipmentCheckpoint(models.Model):
    """
    Entity — Lịch sử trạng thái lộ trình (thay thế cho tracking real-time map).
    """
    shipment = models.ForeignKey(Shipment, related_name='checkpoints', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Shipment.Status.choices)
    location = models.CharField(max_length=255, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shipment_checkpoint'
        ordering = ['timestamp']
