from django.urls import path
from . import views

urlpatterns = [
    path('checkout', views.checkout),
    path('checkout/saga', views.checkout),
    path('customer/<int:customer_id>', views.my_orders),
    path('<int:order_id>/items', views.order_items),
    path('<int:order_id>/status', views.update_status),
    path('<int:order_id>', views.get_order),
    path('stats/summary', views.stats_summary),
    path('', views.all_orders),
]
