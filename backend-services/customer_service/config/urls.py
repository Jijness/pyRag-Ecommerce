from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime


@api_view(['GET'])
def health(request):
    return Response({'status': 'ok', 'service': 'customer_service', 'timestamp': datetime.utcnow().isoformat()})


urlpatterns = [
    path('health', health),
    path('', include('customers.urls')),
]
