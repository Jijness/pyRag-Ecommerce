from django.urls import path
from . import views

urlpatterns = [
    path('<int:customer_id>', views.view_cart),
    path('<int:customer_id>/add', views.add_to_cart),
    path('<int:customer_id>/item/<int:item_id>/quantity', views.update_cart_quantity),
    path('<int:customer_id>/item/<int:item_id>', views.remove_cart_item),
    path('<int:customer_id>/clear', views.clear_cart),
    path('<int:customer_id>/summary', views.cart_summary),
]
