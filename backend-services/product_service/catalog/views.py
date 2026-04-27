from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from datetime import datetime

from .models import Category, Product, Review, Rating
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, RatingSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [AllowAny]

from django.db.models import Q

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-id')
        q = self.request.query_params.get('q', None)
        if q:
            queryset = queryset.filter(name__icontains=q)
        
        category_id = self.request.query_params.get('category_id', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
            
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            skip = int(request.query_params.get('skip', 0))
            limit = int(request.query_params.get('limit', 40))
            queryset = queryset[skip:skip+limit]
        except ValueError:
            pass
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        product = self.get_object()
        reviews = Review.objects.filter(product=product).order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def ratings(self, request, pk=None):
        product = self.get_object()
        ratings = Rating.objects.filter(product=product).order_by('-created_at')
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)

class HealthView(views.APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({"status": "ok", "service": "product_service", "timestamp": datetime.utcnow().isoformat()})

class MetricsView(views.APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({
            "service": "product_service",
            "bounded_context": "catalog",
            "total_products": Product.objects.count()
        })
