# Create your tasks here
from datetime import timedelta, datetime, UTC

import stripe
from celery import shared_task
from django.conf import settings

from borrowing.models import Borrowing
from payment.models import Payment


@shared_task
def auto_cancel_unpaid_borrowings():
    stripe.api_key = settings.STRIPE_SECRET_KEY

    fifteen_minutes_ago = datetime.now(UTC) - timedelta(minutes=15)
    unpaid_borrowings = Borrowing.objects.filter(
        created_at__lt=fifteen_minutes_ago,
        payments__status=Payment.Status.PENDING
    )

    for borrowing in unpaid_borrowings:
        payment = borrowing.payments.first()
        if payment:
            payment.status = Payment.Status.EXPIRED
            payment.save()

            # Повертаємо книгу з резерву
            borrowing.book.is_reserved = False
            borrowing.book.save()