import os

from django.dispatch import receiver
from dotenv import load_dotenv

from notification.signals import notification
from notification.utils import send_message


load_dotenv()

@receiver(notification)
def notify(sender, message: str, chat_id: int = None, **kwargs):
    if kwargs.get("to_admin_chat", None):
        chat_id = os.environ.get("CHAT_ID")
    send_message.delay(chat_id, message)
