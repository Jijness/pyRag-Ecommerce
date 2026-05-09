from django.urls import path
from .views import ShipmentListView, ShipmentDetailView, AssignCourierView, UpdateShipmentStatusView

urlpatterns = [
    path('', ShipmentListView.as_view()),
    path('<int:order_id>', ShipmentDetailView.as_view()),
    path('<int:order_id>/assign', AssignCourierView.as_view()),
    path('<int:order_id>/status', UpdateShipmentStatusView.as_view()),
]
