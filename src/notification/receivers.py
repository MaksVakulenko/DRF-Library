from django.dispatch import receiver

from notification.signals import notification
from notification.utils import send_message


@receiver(notification)
def notify(sender, chat_id: int, message: str, **kwargs):
    send_message(chat_id, message)
