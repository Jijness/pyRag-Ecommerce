from django.urls import path
from .views import health, list_sales, add_search_history, get_recently_viewed, add_recently_viewed

urlpatterns = [
    path('health', health),
    path('sales', list_sales),
    path('search-history', add_search_history),
    path('recently-viewed/<int:customer_id>', get_recently_viewed),
    path('recently-viewed', add_recently_viewed),
]
