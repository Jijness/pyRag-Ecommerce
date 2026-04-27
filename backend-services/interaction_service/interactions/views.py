from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from datetime import datetime
from .models import LoyaltyPoints, GiftCard


class LoyaltySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyPoints
        fields = '__all__'


class GiftCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCard
        fields = '__all__'


@api_view(['GET'])
def health(request):
    return Response({'status': 'ok', 'service': 'interaction_service', 'timestamp': datetime.utcnow().isoformat()})


@api_view(['GET'])
def get_loyalty(request, customer_id):
    lp, _ = LoyaltyPoints.objects.get_or_create(customer_id=customer_id)
    return Response(LoyaltySerializer(lp).data)


@api_view(['POST'])
def add_loyalty_points(request, customer_id):
    lp, _ = LoyaltyPoints.objects.get_or_create(customer_id=customer_id)
    pts = request.data.get('points', 0)
    lp.points += int(pts)
    # Auto-upgrade tier
    if lp.points >= 5000:
        lp.tier = 'Platinum'
    elif lp.points >= 2000:
        lp.tier = 'Gold'
    elif lp.points >= 500:
        lp.tier = 'Silver'
    else:
        lp.tier = 'Bronze'
    lp.save()
    return Response(LoyaltySerializer(lp).data)


@api_view(['GET'])
def get_gift_card(request, code):
    gc = GiftCard.objects.filter(code=code).first()
    if not gc:
        return Response({'detail': 'Gift card không tồn tại'}, status=404)
    return Response(GiftCardSerializer(gc).data)


@api_view(['POST'])
def create_gift_card(request):
    s = GiftCardSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    data = s.validated_data
    if 'remaining_amount' not in data or data.get('remaining_amount') is None:
        data['remaining_amount'] = data.get('amount', 0)
    gc = GiftCard.objects.create(**data)
    return Response(GiftCardSerializer(gc).data, status=201)
