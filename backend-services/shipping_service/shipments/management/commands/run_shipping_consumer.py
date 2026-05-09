import json
import logging
import pika
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from shipments.models import Shipment, ShipmentCheckpoint

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Starts RabbitMQ consumer for Shipping Service'

    def handle(self, *args, **options):
        params = pika.URLParameters(settings.RABBITMQ_URL)
        conn = pika.BlockingConnection(params)
        channel = conn.channel()

        channel.exchange_declare(exchange='shopx', exchange_type='topic', durable=True)
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        # Bind event
        channel.queue_bind(exchange='shopx', queue=queue_name, routing_key='order.created')

        def callback(ch, method, properties, body):
            event = method.routing_key
            try:
                data = json.loads(body)
                if event == 'order.created':
                    self.process_order_created(data)
                
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.error(f"[shipping_consumer] Error processing {event}: {e}")
                ch.basic_ack(delivery_tag=method.delivery_tag)

        self.stdout.write(self.style.SUCCESS('Starting shipping consumer...'))
        channel.basic_consume(queue=queue_name, on_message_callback=callback)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        conn.close()

    @transaction.atomic
    def process_order_created(self, data):
        """
        Xử lý sự kiện order.created: Tạo Shipment.
        Nếu payment_method là COD -> PROCESSING luôn.
        Nếu ONLINE -> AWAITING_PAYMENT.
        """
        order_id = data.get('order_id')
        customer_id = data.get('customer_id')
        address = data.get('shipping_address')
        method = data.get('payment_method')

        if not all([order_id, customer_id, address]):
            logger.warning(f"Invalid order.created event data for shipping: {data}")
            return

        status = Shipment.Status.PROCESSING if method == 'COD' else Shipment.Status.AWAITING_PAYMENT

        shipment, created = Shipment.objects.get_or_create(
            order_id=order_id,
            defaults={
                'customer_id': customer_id,
                'shipping_address': address,
                'status': status
            }
        )
        if created:
            ShipmentCheckpoint.objects.create(
                shipment=shipment,
                status=status,
                note="Shipment initialized via order.created event"
            )
            logger.info(f"Created {status} Shipment for order={order_id}")
        else:
            logger.info(f"Shipment for order={order_id} already exists.")
