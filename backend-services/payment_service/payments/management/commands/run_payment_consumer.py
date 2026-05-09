import json
import logging
import pika
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from payments.models import Payment, TransactionLog

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Starts RabbitMQ consumer for Payment Service'

    def handle(self, *args, **options):
        params = pika.URLParameters(settings.RABBITMQ_URL)
        conn = pika.BlockingConnection(params)
        channel = conn.channel()

        # Tạo queue và bind vào exchange shopx
        channel.exchange_declare(exchange='shopx', exchange_type='topic', durable=True)
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        # Bind các routing keys: order.created
        channel.queue_bind(exchange='shopx', queue=queue_name, routing_key='order.created')

        def callback(ch, method, properties, body):
            event = method.routing_key
            try:
                data = json.loads(body)
                if event == 'order.created':
                    self.process_order_created(data)
                
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"[payment_consumer] Error processing {event}: {e}")
                # Requeue hoặc đưa vào dead-letter queue (trong bài lab đơn giản thì ack luôn để khỏi lặp vô tận)
                ch.basic_ack(delivery_tag=method.delivery_tag)

        self.stdout.write(self.style.SUCCESS('Starting payment consumer...'))
        channel.basic_consume(queue=queue_name, on_message_callback=callback)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        conn.close()

    @transaction.atomic
    def process_order_created(self, data):
        """
        Xử lý sự kiện order.created:
        Tạo bản ghi Payment ở trạng thái PENDING.
        """
        order_id = data.get('order_id')
        customer_id = data.get('customer_id')
        total_price = data.get('total_price')
        payment_method = data.get('payment_method')

        if not all([order_id, customer_id, total_price, payment_method]):
            logger.warning(f"Invalid order.created event data: {data}")
            return

        # Map payment method string sang Enum của Payment
        method_map = {
            'ONLINE': Payment.MethodType.ONLINE,
            'COD': Payment.MethodType.COD,
            'GIFT_CARD': Payment.MethodType.GIFT_CARD,
        }
        method_type = method_map.get(payment_method.upper(), Payment.MethodType.ONLINE)

        payment, created = Payment.objects.get_or_create(
            order_id=order_id,
            defaults={
                'customer_id': customer_id,
                'amount': total_price,
                'method_type': method_type,
                'status': Payment.Status.PENDING
            }
        )
        if created:
            TransactionLog.objects.create(
                payment=payment,
                event_type=TransactionLog.EventType.INITIATED,
                response_message="Payment initialized via order.created event"
            )
            logger.info(f"Created pending Payment for order={order_id}")
        else:
            logger.info(f"Payment for order={order_id} already exists.")
