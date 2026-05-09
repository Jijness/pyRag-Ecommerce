from django.urls import path
from .views import CartDetailView, CartItemListView, CartItemDetailView, CartClearView, CartDeactivateView

urlpatterns = [
    path('', CartDetailView.as_view()),                        # GET  /cart/
    path('items', CartItemListView.as_view()),                  # POST /cart/items
    path('items/<int:item_id>', CartItemDetailView.as_view()),  # PATCH/DELETE /cart/items/<id>
    path('clear', CartClearView.as_view()),                     # DELETE /cart/clear
    path('<int:cart_id>/deactivate', CartDeactivateView.as_view()),  # PATCH (internal)
]
