from django.urls import path
from .views import health, list_banners, create_banner, list_collections, create_collection, list_blog, create_blog

urlpatterns = [
    path('health', health),
    path('banners', list_banners),
    path('banners/create', create_banner),
    path('collections', list_collections),
    path('collections/create', create_collection),
    path('blog', list_blog),
    path('blog/create', create_blog),
]
