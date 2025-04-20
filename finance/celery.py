import os

import django
from celery import Celery, bootsteps
from kombu import Consumer, Exchange, Queue

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance.settings")
django.setup()

from django.conf import settings

from .logger import logger
from perfil.utils import check_if_user_exists, create_user


app = Celery("finance")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


with app.pool.acquire(block=False) as conn:
    exchange_sso_users = Exchange(
        name=f"users_events_sso_{settings.SUFIX}",
        type="direct",
        durable=True,
        channel=conn,
    )
    exchange_sso_users.declare()

    exchange_finance_users = Exchange(
        name=f"users_events_finance_{settings.SUFIX}",
        type="direct",
        durable=True,
        channel=conn,
    )
    exchange_finance_users.declare()

    queue_users = Queue(
        name=f"finance_users_sso_{settings.SUFIX}",
        exchange=exchange_sso_users,
        routing_key=settings.SSO_CLIENT_ID,
        channel=conn,
        durable=True,
        message_ttl=60000,
    )
    queue_users.declare()


class GeneralConsumerStep(bootsteps.ConsumerStep):
    def get_consumers(self, channel):
        return [
            Consumer(
                channel=channel,
                queues=[queue_users],
                callbacks=[self.handle_message_users],
                accept=["json"],
            )
        ]

    def handle_message_users(self, body, message):
        logger.bind(body=body).info("handle_message_users")
        user_exists = check_if_user_exists(body["username"])
        if not user_exists:
            user = create_user(
                username=body["username"],
                email=body["email"]
            )
            if user:
                logger.bind(user=user).info("User created successfully")
            else:
                logger.error("Failed to create user")
        message.ack()


app.steps["consumer"].add(GeneralConsumerStep)
