from django.urls import path
from .views import health, list_notifications, create_notification, mark_read

urlpatterns = [
    path('health', health),
    path('notifications/<int:customer_id>', list_notifications),
    path('notifications', create_notification),
    path('notifications/<int:notification_id>/read', mark_read),
]
