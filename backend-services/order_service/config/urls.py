from django.urls import path, include
from django.http import JsonResponse
from datetime import datetime

def health(request):
    return JsonResponse({"status": "ok", "service": "order_service", "timestamp": datetime.utcnow().isoformat()})

urlpatterns = [
    path('health', health),
    path('orders/', include('orders.urls')),
]
