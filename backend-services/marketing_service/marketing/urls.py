from django.urls import path
from .views import (
    health, list_coupons, create_coupon, validate_coupon,
    list_promotions, create_promotion,
    list_tiers, seed_tiers,
    list_flash_sales, create_flash_sale,
    referral
)

urlpatterns = [
    path('health', health),
    path('coupons', list_coupons),
    path('coupons/create', create_coupon),
    path('coupons/validate/<str:code>', validate_coupon),
    path('promotions', list_promotions),
    path('promotions/create', create_promotion),
    path('tiers', list_tiers),
    path('tiers/seed', seed_tiers),
    path('flash-sales', list_flash_sales),
    path('flash-sales/create', create_flash_sale),
    path('referrals/<int:customer_id>', referral),
]
