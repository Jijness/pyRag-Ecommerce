from rest_framework import serializers
from .models import Shipment, ShipmentCheckpoint
from couriers.serializers import CourierSerializer

class ShipmentCheckpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentCheckpoint
        fields = ['id', 'status', 'location', 'note', 'timestamp']

class ShipmentSerializer(serializers.ModelSerializer):
    checkpoints = ShipmentCheckpointSerializer(many=True, read_only=True)
    courier = CourierSerializer(read_only=True)

    class Meta:
        model = Shipment
        fields = [
            'id', 'order_id', 'customer_id', 'shipping_address', 'status',
            'tracking_number', 'shipping_fee', 'created_at', 'shipped_at', 'delivered_at',
            'courier', 'checkpoints'
        ]
