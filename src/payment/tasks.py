from datetime import timedelta

import stripe
from celery import shared_task
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from borrowing.models import Borrowing
from payment.models import Payment


@shared_task
@transaction.atomic
def auto_cancel_unpaid_borrowings():
    stripe.api_key = settings.STRIPE_SECRET_KEY

    fifteen_minutes_ago = timezone.now() - timedelta(minutes=2)
    unpaid_borrowings = Borrowing.objects.filter(
        borrow_date__lt=fifteen_minutes_ago,
        payments__status=Payment.Status.PENDING
    )

    for borrowing in unpaid_borrowings:
        payment = borrowing.payments.filter(status=Payment.Status.PENDING, type=Payment.Type.PAYMENT).first()
        if payment:
            payment.status = Payment.Status.EXPIRED
            payment.save()

            # Return the book to inventory
            borrowing.book.inventory += 1
            borrowing.book.save()

            # Delete the borrowing record
            borrowing.delete()
