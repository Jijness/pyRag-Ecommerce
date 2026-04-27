from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from django.utils import timezone
from .models import CustomerProfile, Address, Wishlist, WishlistItem, Newsletter

# ── Serializers ────────────────────────────────────────
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class WishlistItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='book_id', read_only=True)
    class Meta:
        model = WishlistItem
        fields = ['id', 'wishlist_id', 'book_id', 'product_id', 'added_at']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = '__all__'

# ── Views ──────────────────────────────────────────────
@api_view(['GET'])
def get_profile(request, customer_id):
    p = CustomerProfile.objects.filter(customer_id=customer_id).first()
    if not p:
        return Response({'detail': 'Not found'}, status=404)
    return Response(ProfileSerializer(p).data)

@api_view(['POST'])
def create_profile(request):
    data = request.data
    cid = data.get('customer_id')
    p, created = CustomerProfile.objects.get_or_create(customer_id=cid)
    p.phone = data.get('phone', p.phone)
    p.avatar_url = data.get('avatar_url', p.avatar_url)
    p.bio = data.get('bio', p.bio)
    p.save()
    return Response(ProfileSerializer(p).data, status=201 if created else 200)

@api_view(['PUT'])
def update_profile(request, customer_id):
    p = CustomerProfile.objects.filter(customer_id=customer_id).first()
    if not p:
        return Response({'detail': 'Not found'}, status=404)
    for field in ['phone', 'avatar_url', 'bio', 'date_of_birth', 'membership_tier']:
        if field in request.data:
            setattr(p, field, request.data[field])
    p.save()
    return Response(ProfileSerializer(p).data)

@api_view(['GET'])
def get_wishlist(request, customer_id):
    wishlist = Wishlist.objects.filter(customer_id=customer_id).first()
    if not wishlist:
        return Response({'customer_id': customer_id, 'items': []})
    items = WishlistItem.objects.filter(wishlist=wishlist)
    return Response({
        'id': wishlist.id,
        'customer_id': customer_id,
        'items': [{'id': i.id, 'product_id': i.book_id, 'book_id': i.book_id, 'added_at': i.added_at} for i in items]
    })

@api_view(['POST'])
def toggle_wishlist(request, customer_id, product_id):
    wishlist, _ = Wishlist.objects.get_or_create(customer_id=customer_id)
    item = WishlistItem.objects.filter(wishlist=wishlist, book_id=product_id).first()
    if item:
        item.delete()
        return Response({'action': 'removed', 'product_id': product_id})
    WishlistItem.objects.create(wishlist=wishlist, book_id=product_id)
    return Response({'action': 'added', 'product_id': product_id})

@api_view(['GET'])
def get_addresses(request, customer_id):
    profile = CustomerProfile.objects.filter(customer_id=customer_id).first()
    if not profile:
        return Response([])
    addresses = Address.objects.filter(customer_profile=profile)
    return Response(AddressSerializer(addresses, many=True).data)

@api_view(['POST'])
def add_address(request):
    data = request.data
    cid = data.get('customer_id')
    profile, _ = CustomerProfile.objects.get_or_create(customer_id=cid)
    addr = Address.objects.create(
        customer_profile=profile,
        street=data.get('street', ''),
        city=data.get('city', ''),
        state=data.get('state'),
        zip_code=data.get('zip_code'),
        country=data.get('country', 'Vietnam'),
        is_default=data.get('is_default', False)
    )
    return Response(AddressSerializer(addr).data, status=201)

@api_view(['POST'])
def subscribe_newsletter(request):
    email = request.data.get('email')
    cid = request.data.get('customer_id')
    if not email:
        return Response({'detail': 'Email required'}, status=400)
    n, created = Newsletter.objects.get_or_create(email=email, defaults={'customer_id': cid})
    if not created:
        n.is_subscribed = True
        n.save()
    return Response({'message': 'Subscribed', 'email': email})

@api_view(['GET'])
def health(request):
    from datetime import datetime
    return Response({'status': 'ok', 'service': 'customer_service', 'timestamp': datetime.utcnow().isoformat()})
