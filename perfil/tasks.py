from celery import shared_task
from django.conf import settings

from finance.celery import app
from finance.logger import logger


@shared_task
@logger.catch
def publish_user_event(user_data):
    """
    Publishes a user event to the users_events_finance exchange.

    Args:
        user_data (dict): The user data to publish.
    """
    with app.producer_pool.acquire(block=True) as producer:
        producer.publish(
            user_data,
            exchange=f"users_events_finance_{settings.SUFIX}",
            routing_key=settings.SSO_CLIENT_ID,
            serializer="json",
        )
        logger.bind(user=user_data).info("User event published")
