from django.urls import path
from .views import GiftCardListView, ApplyGiftCardView

urlpatterns = [
    path('', GiftCardListView.as_view()),
    path('apply', ApplyGiftCardView.as_view()),
]
