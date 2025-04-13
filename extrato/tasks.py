from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from loguru import logger


@shared_task
def send_email_task(subject, message, recipient_list):
    """Task de envio de emails

    Args:
        subject (str): Assunto
        message (str): Corpo do email
        recipient_list (str): Destinatario
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False
    )

    logger.bind(
        assunto=subject, mensagem=message, destinatario=recipient_list
    ).info("Email enviado com sucesso!")
