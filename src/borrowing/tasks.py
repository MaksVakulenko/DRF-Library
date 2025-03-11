from datetime import datetime

from celery import shared_task

from borrowing.models import Borrowing
from library_service.settings import FRONTEND_URL
from notification.signals import notification
from user.tasks import send_verification_email_task
from library_service.messages import get_message_overdue_borrowings, get_email_overdue_message


@shared_task
def check_overdue_borrowings():
    today = datetime.now().date()
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=today,
        actual_return_date__isnull=True
    )
    if not overdue_borrowings:
        return notification.send(
            sender=None,
            message="No borrowings overdue today!",
            to_admin_chat=True
        )

    for borrowing in overdue_borrowings:
        admin_message = get_message_overdue_borrowings(borrowing)
        notification.send(sender=None, message=admin_message, to_admin_chat=True)
        today = datetime.now().date()
        days_expired = (today - borrowing.expected_return_date).days
        fine = int((borrowing.book.daily_fee * days_expired) * 100) * 2

        email_message = get_email_overdue_message(borrowing=borrowing, days_expired=days_expired, fine=fine, frontend_url=FRONTEND_URL)

        send_verification_email_task.delay(
            subject="Overdue borrowing",
            message=email_message,
            recipient_list=[borrowing.user.email]
        )
