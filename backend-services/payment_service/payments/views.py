"""
Payment Service — Application Layer (Views)
Xử lý: Thanh toán Online (giả lập), COD, GiftCard, Refund.
RabbitMQ consumer được khởi động qua management command.
"""
import uuid
import logging
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Payment, TransactionLog, Refund
from .serializers import PaymentSerializer, RefundSerializer

logger = logging.getLogger(__name__)


def _log_transaction(payment, event_type, ref=None, msg=None):
    TransactionLog.objects.create(
        payment=payment,
        event_type=event_type,
        gateway_transaction_id=ref,
        response_message=msg,
    )


class PaymentStatusView(APIView):
    """GET /payments/<order_id>  — Xem trạng thái thanh toán."""
    def get(self, request, order_id):
        payment = get_object_or_404(Payment, order_id=order_id)
        return Response(PaymentSerializer(payment).data)


class OnlinePaymentView(APIView):
    """
    UC03: Thanh toán Online (giả lập PayOS/Momo/VietQR).
    POST /payments/<order_id>/process
    Body: { "action": "success" | "fail" }

    Luồng chính (action=success):  Payment.status = SUCCESS → publish payment.completed
    Luồng thay thế (action=fail):  Payment.status = FAILED  → publish payment.failed
    """
    def post(self, request, order_id):
        payment = get_object_or_404(Payment, order_id=order_id, status=Payment.Status.PENDING)
        action = request.data.get('action', 'success')

        if action == 'success':
            ref = f"SIMULATED_TXN_{uuid.uuid4().hex[:12].upper()}"
            payment.status = Payment.Status.SUCCESS
            payment.gateway_ref = ref
            payment.paid_at = timezone.now()
            payment.save()
            _log_transaction(payment, TransactionLog.EventType.CONFIRMED, ref=ref,
                             msg="Simulated online payment success")
            # Publish event
            _publish_payment_event(payment, 'payment.completed')
            logger.info(f"[payment_service] Order {order_id} — payment SUCCESS, ref={ref}")
            return Response({"status": "SUCCESS", "gateway_ref": ref})

        else:  # fail
            payment.status = Payment.Status.FAILED
            payment.save()
            _log_transaction(payment, TransactionLog.EventType.FAILED,
                             msg="Simulated online payment failed by user")
            _publish_payment_event(payment, 'payment.failed')
            logger.warning(f"[payment_service] Order {order_id} — payment FAILED")
            return Response({"status": "FAILED"})


class RefundView(APIView):
    """
    UC05: Yêu cầu hoàn tiền.
    POST /payments/<order_id>/refund
    PATCH /payments/refunds/<refund_id>  — Admin duyệt
    """
    def post(self, request, order_id):
        payment = get_object_or_404(Payment, order_id=order_id, status=Payment.Status.SUCCESS)
        if hasattr(payment, 'refund'):
            return Response({"error": "Refund already requested."}, status=400)
        refund = Refund.objects.create(
            payment=payment,
            order_id=order_id,
            amount=payment.amount,
            reason=request.data.get('reason', ''),
        )
        return Response(RefundSerializer(refund).data, status=201)

    def patch(self, request, refund_id):
        refund = get_object_or_404(Refund, pk=refund_id)
        action = request.data.get('action')  # 'approve' | 'reject'
        admin_id = request.headers.get('X-Admin-Id')

        if action == 'approve':
            refund.status = Refund.Status.APPROVED
            refund.payment.status = Payment.Status.REFUNDED
            refund.payment.save()
            _log_transaction(refund.payment, TransactionLog.EventType.REFUNDED)
        elif action == 'reject':
            refund.status = Refund.Status.REJECTED
        else:
            return Response({"error": "action must be 'approve' or 'reject'"}, status=400)

        refund.resolved_at = timezone.now()
        refund.resolved_by = int(admin_id) if admin_id else None
        refund.save()
        return Response(RefundSerializer(refund).data)


class TransactionListView(APIView):
    """GET /payments/transactions  — Staff/Admin xem lịch sử giao dịch."""
    def get(self, request):
        logs = TransactionLog.objects.select_related('payment').order_by('-logged_at')[:100]
        data = [
            {
                'id': l.pk,
                'order_id': l.payment.order_id,
                'event_type': l.event_type,
                'gateway_transaction_id': l.gateway_transaction_id,
                'response_message': l.response_message,
                'logged_at': l.logged_at,
            }
            for l in logs
        ]
        return Response(data)


def _publish_payment_event(payment: Payment, routing_key: str):
    """Publish event đến RabbitMQ."""
    try:
        import pika, json
        from django.conf import settings

        params = pika.URLParameters(settings.RABBITMQ_URL)
        conn = pika.BlockingConnection(params)
        ch = conn.channel()
        ch.exchange_declare(exchange='shopx', exchange_type='topic', durable=True)
        body = json.dumps({
            'event': routing_key,
            'order_id': payment.order_id,
            'payment_id': payment.pk,
            'status': payment.status,
            'amount': payment.amount,
            'method_type': payment.method_type,
        })
        ch.basic_publish(exchange='shopx', routing_key=routing_key,
                         body=body.encode(),
                         properties=pika.BasicProperties(delivery_mode=2))
        conn.close()
        logger.info(f"[payment_service] Published: {routing_key} for order={payment.order_id}")
    except Exception as e:
        logger.error(f"[payment_service] RabbitMQ publish failed: {e}")
