from django.urls import path, include
from django.http import JsonResponse
from datetime import datetime

def health(request):
    return JsonResponse({"status": "ok", "service": "cart_service", "timestamp": datetime.utcnow().isoformat()})

urlpatterns = [
    path('health', health),
    path('metrics', include('django_prometheus.urls')),
    path('cart/', include('cart.urls')),
]
