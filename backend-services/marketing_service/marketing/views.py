from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from datetime import datetime
from django.utils import timezone
import uuid
from .models import Coupon, Promotion, MembershipTier, FlashSale, ReferralCode, Bundle, Discount


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'


class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipTier
        fields = '__all__'


class FlashSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashSale
        fields = '__all__'


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = '__all__'


@api_view(['GET'])
def health(request):
    return Response({'status': 'ok', 'service': 'marketing_service', 'timestamp': datetime.utcnow().isoformat()})


# ── COUPON ──────────────────────────────────────────────
@api_view(['GET'])
def list_coupons(request):
    coupons = Coupon.objects.filter(active=True)
    return Response(CouponSerializer(coupons, many=True).data)


@api_view(['POST'])
def create_coupon(request):
    data = request.data.copy()
    data['code'] = data.get('code', '').upper()
    s = CouponSerializer(data=data)
    s.is_valid(raise_exception=True)
    coupon = s.save()
    return Response(CouponSerializer(coupon).data, status=201)


@api_view(['GET'])
def validate_coupon(request, code):
    order_total = float(request.query_params.get('order_total', 0))
    coupon = Coupon.objects.filter(code=code.upper(), active=True).first()
    if not coupon:
        return Response({'detail': 'Mã giảm giá không hợp lệ'}, status=404)
    if coupon.valid_to and coupon.valid_to < timezone.now():
        return Response({'detail': 'Mã giảm giá đã hết hạn'}, status=400)
    if order_total < coupon.min_order_value:
        return Response({'detail': f'Đơn hàng phải tối thiểu {coupon.min_order_value}'}, status=400)
    discount = 0
    if coupon.discount_percent:
        discount = order_total * coupon.discount_percent / 100
    elif coupon.discount_amount:
        discount = coupon.discount_amount
    return Response({'valid': True, 'discount': discount, 'coupon': CouponSerializer(coupon).data})


# ── PROMOTION ────────────────────────────────────────────
@api_view(['GET'])
def list_promotions(request):
    promos = Promotion.objects.filter(is_active=True)
    return Response(PromotionSerializer(promos, many=True).data)


@api_view(['POST'])
def create_promotion(request):
    s = PromotionSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    promo = s.save()
    return Response(PromotionSerializer(promo).data, status=201)


# ── MEMBERSHIP TIER ─────────────────────────────────────
@api_view(['GET'])
def list_tiers(request):
    tiers = MembershipTier.objects.all()
    return Response(TierSerializer(tiers, many=True).data)


@api_view(['POST'])
def seed_tiers(request):
    tiers_data = [
        {'name': 'Bronze',   'min_points': 0,    'discount_percent': 0,   'free_shipping': False},
        {'name': 'Silver',   'min_points': 500,  'discount_percent': 3,   'free_shipping': False},
        {'name': 'Gold',     'min_points': 2000, 'discount_percent': 5,   'free_shipping': True},
        {'name': 'Platinum', 'min_points': 5000, 'discount_percent': 10,  'free_shipping': True},
    ]
    for t in tiers_data:
        MembershipTier.objects.get_or_create(name=t['name'], defaults=t)
    return Response({'message': 'Đã tạo 4 hạng thành viên'})


# ── FLASH SALE ──────────────────────────────────────────
@api_view(['GET'])
def list_flash_sales(request):
    sales = FlashSale.objects.filter(is_active=True)
    return Response(FlashSaleSerializer(sales, many=True).data)


@api_view(['POST'])
def create_flash_sale(request):
    s = FlashSaleSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    sale = s.save()
    return Response(FlashSaleSerializer(sale).data, status=201)


# ── REFERRAL ────────────────────────────────────────────
@api_view(['GET', 'POST'])
def referral(request, customer_id):
    if request.method == 'GET':
        ref = ReferralCode.objects.filter(owner_customer_id=customer_id).first()
        if not ref:
            return Response({'detail': 'Chưa có mã giới thiệu'}, status=404)
        return Response(ReferralSerializer(ref).data)
    # POST – tạo hoặc trả lại mã đang active
    existing = ReferralCode.objects.filter(owner_customer_id=customer_id, is_active=True).first()
    if existing:
        return Response(ReferralSerializer(existing).data)
    code = str(uuid.uuid4()).replace('-', '')[:8].upper()
    ref = ReferralCode.objects.create(code=code, owner_customer_id=customer_id)
    return Response(ReferralSerializer(ref).data, status=201)
