from rest_framework import serializers
from .models import GiftCard

class GiftCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCard
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

class ApplyGiftCardSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)
    order_amount = serializers.FloatField(min_value=0)
