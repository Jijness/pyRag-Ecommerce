import os
import pika
import json
import logging

logger = logging.getLogger(__name__)

RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

def publish_order_created(order_id, customer_id, total_price, pay_method, ship_method):
    try:
        parameters = pika.URLParameters(RABBITMQ_URL)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        
        channel.exchange_declare(exchange='ecommerce_exchange', exchange_type='topic', durable=True)
        
        payload = {
            "order_id": order_id,
            "customer_id": customer_id,
            "total_price": total_price,
            "pay_method": pay_method,
            "ship_method": ship_method
        }
        
        channel.basic_publish(
            exchange='ecommerce_exchange',
            routing_key='order.created',
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        logger.info(f"Published order.created for Order {order_id}")
        connection.close()
    except Exception as e:
        logger.error(f"Failed to publish order event: {e}")
