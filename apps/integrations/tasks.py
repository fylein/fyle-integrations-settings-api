import pika
import json
import os
import logging
from django_q.models import Schedule
from datetime import datetime

logger = logging.getLogger(__name__)
logger.level = logging.INFO

def publish_to_rabbitmq():
    """
    Publish message to RabbitMQ
    """
    try:
        rabbitmq_url = os.environ.get('RABBITMQ_URL')
        connection = pika.BlockingConnection(
            parameters=pika.URLParameters(rabbitmq_url)
        )
        channel = connection.channel()

        channel.queue_declare(queue='upload_queue', durable=True)

        channel.basic_publish(
            exchange=os.environ.get('RABBITMQ_EXCHANGE'),
            routing_key='upload.s3',
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

        connection.close()
        logger.info('Successfully published message to RabbitMQ')

    except Exception as e:
        logger.error('Error publishing to RabbitMQ: %s', str(e))
        raise

def ensure_upload_schedule():
    """
    Ensure the upload schedule exists
    """
    Schedule.objects.update_or_create(
        func='apps.integrations.queue.publish_to_rabbitmq',
        defaults={
            'schedule_type': Schedule.MINUTES,
            'minutes': 10,
            'next_run': datetime.now()
        }
    )
