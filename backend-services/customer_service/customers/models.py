from django.db import models
from django.utils import timezone

class CustomerProfile(models.Model):
    customer_id = models.IntegerField(unique=True)
    phone = models.CharField(max_length=255, null=True)
    date_of_birth = models.DateTimeField(null=True)
    avatar_url = models.CharField(max_length=255, null=True)
    bio = models.TextField(null=True)
    points = models.IntegerField(default=0)
    membership_tier = models.CharField(max_length=255, default='Bronze')
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'customer_profile'

class Address(models.Model):
    customer_profile = models.ForeignKey(CustomerProfile, related_name='addresses', on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, null=True)
    zip_code = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, default='Vietnam')
    is_default = models.BooleanField(default=False)
    class Meta:
        db_table = 'address'

class Wishlist(models.Model):
    customer_id = models.IntegerField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'wishlist'

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, related_name='items', on_delete=models.CASCADE)
    book_id = models.IntegerField()
    added_at = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'wishlist_item'

class Newsletter(models.Model):
    email = models.CharField(max_length=255, unique=True)
    customer_id = models.IntegerField(null=True)
    is_subscribed = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(default=timezone.now)
    unsubscribed_at = models.DateTimeField(null=True)
    class Meta:
        db_table = 'newsletter'

class CustomerPreference(models.Model):
    customer_id = models.IntegerField(unique=True)
    favorite_genres = models.CharField(max_length=255, null=True)
    favorite_authors = models.CharField(max_length=255, null=True)
    preferred_language = models.CharField(max_length=255, null=True)
    preferred_format = models.CharField(max_length=255, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'customer_preference'
