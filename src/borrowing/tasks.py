from datetime import datetime

from celery import shared_task

from borrowing.models import Borrowing
from notification.signals import notification
from user.tasks import send_verification_email_task


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
        admin_message = (
            f"📚 Overdue Borrowing Alert!\n\n"
            f"👤 User: {borrowing.user}\n"
            f"🔹 Book: {borrowing.book}\n"
            f"📅 Borrowed on: {borrowing.borrow_date.strftime('%B %d, %Y')}\n"
            f"📅 Expected return: {borrowing.expected_return_date.strftime('%B %d, %Y')}"
        )
        notification.send(sender=None, message=admin_message, to_admin_chat=True)
        today = datetime.now().date()
        days_expired = (today - borrowing.expected_return_date).days
        fine = int((borrowing.book.daily_fee * days_expired) * 100) * 2

        email_message = (
            f"Hello, {borrowing.user.first_name}!\n\n"
            f"We noticed that the book \"{borrowing.book.title}\" you borrowed on "
            f"{borrowing.borrow_date.strftime('%B %d, %Y')} was due for return on "
            f"{borrowing.expected_return_date.strftime('%B %d, %Y')}.\n\n"
            f"As of today, it is overdue by {days_expired} day(s). Please return the book as soon as possible to avoid further penalties.\n\n"
            f"A fine of ${fine / 100:.2f} has been applied to your account.\n\n"
            "If you have any questions, feel free to reach out.\n\n"
            "Thank you for your cooperation!\n\n"
            "Best regards,\n"
            "Your Library Team 📚"
        )

        send_verification_email_task.delay(
            subject="Overdue borrowing",
            message=email_message,
            recipient_list=[borrowing.user.email]
        )