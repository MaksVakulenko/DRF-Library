from datetime import datetime

from celery import shared_task

from borrowing.models import Borrowing
from notification.signals import notification
from notification.utils import send_message


@shared_task
def check_overdue_borrowings():
    today = datetime.now().date()
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=today,
        actual_return_date__isnull=True
    )
    if not overdue_borrowings:
        return notification.send(sender=None, message="No borrowings overdue today!", to_admin_chat=True)

    for borrowing in overdue_borrowings:
        message = (
            f"📚 Overdue Borrowing Alert!\n\n"
            f"👤 User: {borrowing.user}\n"
            f"🔹 Book: {borrowing.book}\n"
            f"📅 Borrowed on: {borrowing.borrow_date.strftime('%B %d, %Y')}\n"
            f"📅 Expected return: {borrowing.expected_return_date.strftime('%B %d, %Y')}"
        )
        notification.send(sender=None, message=message, to_admin_chat=True)
