from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from datetime import datetime
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


@api_view(['GET'])
def health(request):
    return Response({'status': 'ok', 'service': 'notification_service', 'timestamp': datetime.utcnow().isoformat()})


@api_view(['GET'])
def list_notifications(request, customer_id):
    notifs = Notification.objects.filter(customer_id=customer_id).order_by('-created_at')
    return Response(NotificationSerializer(notifs, many=True).data)


@api_view(['POST'])
def create_notification(request):
    s = NotificationSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    notif = s.save()
    return Response(NotificationSerializer(notif).data, status=201)


@api_view(['PATCH'])
def mark_read(request, notification_id):
    notif = Notification.objects.filter(id=notification_id).first()
    if not notif:
        return Response({'detail': 'Không tìm thấy thông báo'}, status=404)
    notif.is_read = True
    notif.save()
    return Response({'id': notification_id, 'is_read': True})
