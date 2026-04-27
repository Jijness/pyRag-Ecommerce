from django.urls import path
from .views import (
    health,
    list_suppliers, create_supplier,
    list_pos, create_po, update_po_status,
    list_warehouses, create_warehouse,
    list_logs, add_log,
    list_alerts, create_alert, resolve_alert
)

urlpatterns = [
    path('health', health),
    path('suppliers', list_suppliers),
    path('suppliers/create', create_supplier),
    path('purchase-orders', list_pos),
    path('purchase-orders/create', create_po),
    path('purchase-orders/<int:po_id>/status', update_po_status),
    path('warehouses', list_warehouses),
    path('warehouses/create', create_warehouse),
    path('logs', list_logs),
    path('logs/create', add_log),
    path('alerts', list_alerts),
    path('alerts/create', create_alert),
    path('alerts/<int:alert_id>/resolve', resolve_alert),
]
