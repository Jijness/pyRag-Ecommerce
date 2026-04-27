from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'reviews', views.ReviewViewSet)
router.register(r'ratings', views.RatingViewSet)

urlpatterns = [
    path('health', views.HealthView.as_view(), name='health'),
    path('metrics', views.MetricsView.as_view(), name='metrics'),
    path('', include(router.urls)),
]
