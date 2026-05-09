from django.db import models
from django.utils import timezone


class Courier(models.Model):
    """
    Entity — Courier (tài xế giao hàng).
    """
    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE'
        BUSY = 'BUSY'
        OFFLINE = 'OFFLINE'

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    current_location = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'courier'

    def __str__(self):
        return f"Courier({self.name}, status={self.status})"
