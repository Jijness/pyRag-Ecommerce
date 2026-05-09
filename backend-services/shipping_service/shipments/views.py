import logging
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Shipment, ShipmentCheckpoint
from .serializers import ShipmentSerializer
from couriers.models import Courier

logger = logging.getLogger(__name__)

def _publish_shipment_event(shipment: Shipment, routing_key: str):
    try:
        import pika, json
        from django.conf import settings
        params = pika.URLParameters(settings.RABBITMQ_URL)
        conn = pika.BlockingConnection(params)
        ch = conn.channel()
        ch.exchange_declare(exchange='shopx', exchange_type='topic', durable=True)
        body = json.dumps({
            'event': routing_key,
            'order_id': shipment.order_id,
            'shipment_id': shipment.pk,
            'status': shipment.status,
            'tracking_number': shipment.tracking_number,
        })
        ch.basic_publish(exchange='shopx', routing_key=routing_key, body=body.encode())
        conn.close()
    except Exception as e:
        logger.error(f"[shipping_service] RabbitMQ publish failed: {e}")

class ShipmentListView(APIView):
    """GET /shipments  — List (cho Admin/Staff)"""
    def get(self, request):
        status_filter = request.query_params.get('status')
        qs = Shipment.objects.all()
        if status_filter:
            qs = qs.filter(status=status_filter)
        return Response(ShipmentSerializer(qs, many=True).data)

class ShipmentDetailView(APIView):
    """GET /shipments/<order_id>  — Xem trạng thái & lịch sử (Customer)"""
    def get(self, request, order_id):
        shipment = get_object_or_404(Shipment, order_id=order_id)
        return Response(ShipmentSerializer(shipment).data)

class AssignCourierView(APIView):
    """PATCH /shipments/<order_id>/assign — Staff gán Courier"""
    def patch(self, request, order_id):
        shipment = get_object_or_404(Shipment, order_id=order_id)
        courier_id = request.data.get('courier_id')
        courier = get_object_or_404(Courier, pk=courier_id)
        
        shipment.courier = courier
        shipment.save()
        return Response(ShipmentSerializer(shipment).data)

class UpdateShipmentStatusView(APIView):
    """
    PATCH /shipments/<order_id>/status
    Body: {"status": "SHIPPING", "location": "Kho HN", "note": "..."}
    """
    def patch(self, request, order_id):
        shipment = get_object_or_404(Shipment, order_id=order_id)
        new_status = request.data.get('status')
        location = request.data.get('location')
        note = request.data.get('note')

        if new_status not in dict(Shipment.Status.choices):
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        shipment.status = new_status
        if new_status == Shipment.Status.SHIPPING and not shipment.shipped_at:
            shipment.shipped_at = timezone.now()
        elif new_status == Shipment.Status.DELIVERED:
            shipment.delivered_at = timezone.now()

        shipment.save()
        
        # Thêm checkpoint
        ShipmentCheckpoint.objects.create(
            shipment=shipment, status=new_status, location=location, note=note
        )

        # Publish event nếu delivered / failed
        if new_status == Shipment.Status.DELIVERED:
            _publish_shipment_event(shipment, 'shipment.delivered')
        elif new_status == Shipment.Status.FAILED:
            _publish_shipment_event(shipment, 'shipment.failed')

        return Response(ShipmentSerializer(shipment).data)
