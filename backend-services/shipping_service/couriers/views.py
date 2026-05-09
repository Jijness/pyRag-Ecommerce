from rest_framework import viewsets
from .models import Courier
from .serializers import CourierSerializer

class CourierViewSet(viewsets.ModelViewSet):
    """Admin CRUD cho Courier"""
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
