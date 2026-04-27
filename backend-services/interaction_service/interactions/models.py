from django.db import models


class LoyaltyPoints(models.Model):
    customer_id = models.IntegerField(unique=True)
    points = models.IntegerField(default=0)
    tier = models.CharField(max_length=50, default='Bronze')
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'loyalty_points'


class GiftCard(models.Model):
    code = models.CharField(max_length=50, unique=True)
    amount = models.FloatField()
    remaining_amount = models.FloatField()
    issued_to = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'gift_cards'
