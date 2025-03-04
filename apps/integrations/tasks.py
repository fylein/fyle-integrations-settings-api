import pika
import json
import os
import logging
from datetime import datetime
from fyle_accounting_library.rabbitmq.connector import RabbitMQConnection
from fyle_accounting_library.fyle_platform.enums import RoutingKeyEnum

logger = logging.getLogger(__name__)
logger.level = logging.INFO

def publish_to_rabbitmq():
    """
    Publish message to RabbitMQ
    """
    try:
        rabbitmq = RabbitMQConnection.get_instance('integrations_pgevents_exchange')
        rabbitmq.publish(RoutingKeyEnum.UPLOAD_S3.value, {})
        logger.info('Successfully published message to RabbitMQ')

    except Exception as e:
        logger.error('Error publishing to RabbitMQ: %s', str(e))
        raise
