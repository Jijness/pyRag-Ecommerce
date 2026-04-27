from django.urls import path
from .views import health, get_loyalty, add_loyalty_points, get_gift_card, create_gift_card

urlpatterns = [
    path('health', health),
    path('loyalty-points/<int:customer_id>', get_loyalty),
    path('loyalty-points/<int:customer_id>/add', add_loyalty_points),
    path('gift-cards/<str:code>', get_gift_card),
    path('gift-cards', create_gift_card),
]
