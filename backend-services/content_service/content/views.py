from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from datetime import datetime
from .models import Banner, Collection, BlogPost


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'


@api_view(['GET'])
def health(request):
    return Response({'status': 'ok', 'service': 'content_service', 'timestamp': datetime.utcnow().isoformat()})


@api_view(['GET'])
def list_banners(request):
    banners = Banner.objects.filter(is_active=True).order_by('display_order')
    return Response(BannerSerializer(banners, many=True).data)


@api_view(['POST'])
def create_banner(request):
    s = BannerSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    banner = s.save()
    return Response(BannerSerializer(banner).data, status=201)


@api_view(['GET'])
def list_collections(request):
    collections = Collection.objects.filter(is_active=True)
    return Response(CollectionSerializer(collections, many=True).data)


@api_view(['POST'])
def create_collection(request):
    s = CollectionSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    col = s.save()
    return Response(CollectionSerializer(col).data, status=201)


@api_view(['GET'])
def list_blog(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-published_at')
    return Response(BlogPostSerializer(posts, many=True).data)


@api_view(['POST'])
def create_blog(request):
    s = BlogPostSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    post = s.save()
    return Response(BlogPostSerializer(post).data, status=201)
