from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import GiftCard
from .serializers import GiftCardSerializer, ApplyGiftCardSerializer

class GiftCardListView(APIView):
    def get(self, request):
        customer_id = request.headers.get('X-Customer-Id')
        if customer_id:
            cards = GiftCard.objects.filter(issued_to=customer_id)
            return Response(GiftCardSerializer(cards, many=True).data)
        return Response({"error": "Missing X-Customer-Id header"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # Admin issue gift card
        serializer = GiftCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplyGiftCardView(APIView):
    def post(self, request):
        serializer = ApplyGiftCardSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        code = serializer.validated_data['code']
        order_amount = serializer.validated_data['order_amount']

        card = get_object_or_404(GiftCard, code=code)
        
        if not card.is_active:
            return Response({"error": "Gift card is inactive"}, status=status.HTTP_400_BAD_REQUEST)
        
        if card.expires_at and card.expires_at < timezone.now():
            return Response({"error": "Gift card is expired"}, status=status.HTTP_400_BAD_REQUEST)
        
        discount = min(card.remaining_amount, order_amount)
        new_remaining = card.remaining_amount - discount
        
        # Deduct amount
        card.remaining_amount = new_remaining
        if new_remaining == 0:
            card.is_active = False
        card.save()

        return Response({
            "discount_applied": discount,
            "remaining_amount": new_remaining,
            "card_active": card.is_active
        })
