from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.FloatField(null=True, blank=True)
    discount_amount = models.FloatField(null=True, blank=True)
    min_order_value = models.FloatField(default=0)
    max_uses = models.IntegerField(null=True, blank=True)
    used_count = models.IntegerField(default=0)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'coupons'


class Promotion(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    discount_percent = models.FloatField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'promotions'


class MembershipTier(models.Model):
    name = models.CharField(max_length=100)
    min_points = models.IntegerField(default=0)
    discount_percent = models.FloatField(default=0)
    free_shipping = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'membership_tiers'


class FlashSale(models.Model):
    name = models.CharField(max_length=255)
    discount_percent = models.FloatField()
    max_quantity = models.IntegerField(null=True, blank=True)
    sold_quantity = models.IntegerField(default=0)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    product_id = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'flash_sales'


class ReferralCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    owner_customer_id = models.IntegerField()
    reward_points = models.IntegerField(default=100)
    is_active = models.BooleanField(default=True)
    used_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'referral_codes'


class Bundle(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'bundles'


class Discount(models.Model):
    name = models.CharField(max_length=255)
    product_id = models.IntegerField(null=True, blank=True)
    genre_id = models.IntegerField(null=True, blank=True)
    discount_percent = models.FloatField(default=0)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'discounts'
