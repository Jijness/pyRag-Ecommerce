from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from datetime import datetime
import httpx
import logging

logger = logging.getLogger(__name__)

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

    def trigger_ai_sync(self, product):
        try:
            # We call the new /sync-product endpoint in ai_chat_service
            # We run it synchronously for simplicity in this version
            payload = {
                "id": product.id,
                "title": product.name,
                "price": float(product.price),
                "category_id": product.category_id,
                "category_name": product.category.name if product.category else "Unknown",
                "brand_name": "ShopX",
                "description": product.description
            }
            with httpx.Client(timeout=3.0) as client:
                res = client.post("http://ai_chat_service:8012/sync-product", json=payload)
                if res.status_code == 200:
                    logger.info(f"AI sync successful for product {product.id}")
                else:
                    logger.warning(f"AI sync failed: {res.status_code} {res.text}")
        except Exception as e:
            logger.error(f"Error calling ai_chat_service sync: {e}")

    def perform_create(self, serializer):
        product = serializer.save()
        self.trigger_ai_sync(product)

    def perform_update(self, serializer):
        product = serializer.save()
        self.trigger_ai_sync(product)

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
