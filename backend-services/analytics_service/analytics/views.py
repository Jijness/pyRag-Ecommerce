from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from datetime import datetime
from .models import SalesSummary, SearchHistory, RecentlyViewed


class SalesSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesSummary
        fields = '__all__'


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = '__all__'


class RecentlyViewedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentlyViewed
        fields = '__all__'


@api_view(['GET'])
def health(request):
    return Response({'status': 'ok', 'service': 'analytics_service', 'timestamp': datetime.utcnow().isoformat()})


@api_view(['GET'])
def list_sales(request):
    summaries = SalesSummary.objects.order_by('-date')[:30]
    return Response(SalesSummarySerializer(summaries, many=True).data)


@api_view(['POST'])
def add_search_history(request):
    s = SearchHistorySerializer(data=request.data)
    s.is_valid(raise_exception=True)
    item = s.save()
    return Response(SearchHistorySerializer(item).data, status=201)


@api_view(['GET'])
def get_recently_viewed(request, customer_id):
    items = RecentlyViewed.objects.filter(customer_id=customer_id).order_by('-viewed_at')[:20]
    return Response(RecentlyViewedSerializer(items, many=True).data)


@api_view(['POST'])
def add_recently_viewed(request):
    data = request.data
    cid = data.get('customer_id')
    pid = data.get('product_id')
    # Upsert: xóa bản ghi cũ nếu tồn tại rồi tạo mới (để cập nhật viewed_at)
    RecentlyViewed.objects.filter(customer_id=cid, product_id=pid).delete()
    rv = RecentlyViewed.objects.create(customer_id=cid, product_id=pid)
    return Response(RecentlyViewedSerializer(rv).data, status=201)
