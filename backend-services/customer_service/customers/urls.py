from django.urls import path
from .views import (
    get_profile, create_profile, update_profile,
    get_wishlist, toggle_wishlist,
    get_addresses, add_address, subscribe_newsletter, health
)

urlpatterns = [
    path('health', health),
    path('profile', create_profile),
    path('profile/<int:customer_id>', get_profile),
    path('profile/<int:customer_id>/update', update_profile),
    path('wishlist/<int:customer_id>', get_wishlist),
    path('wishlist/<int:customer_id>/toggle/<int:product_id>', toggle_wishlist),
    path('addresses/<int:customer_id>', get_addresses),
    path('addresses', add_address),
    path('newsletter/subscribe', subscribe_newsletter),
]
