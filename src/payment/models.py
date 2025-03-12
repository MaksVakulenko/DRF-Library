import stripe
from django.conf import settings
from django.db import models, transaction
from rest_framework.reverse import reverse


class Payment(models.Model):
    """Model representing a Stripe payment for a borrowing."""

    class Status(models.IntegerChoices):
        PENDING = 0, "Pending"
        PAID = 1, "Paid"
        EXPIRED = -1, "Expired"

    class Type(models.IntegerChoices):
        PAYMENT = 1, "PAYMENT"
        FINE = -1, "FINE"

    borrowing = models.ForeignKey(
        "borrowing.Borrowing", on_delete=models.CASCADE, related_name="payments"
    )
    session_url = models.URLField(max_length=500)  # Stripe checkout session URL
    session_id = models.CharField(max_length=255)  # Stripe session ID
    amount_of_money = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Total payment amount in $USD
    status = models.IntegerField(
        choices=Status.choices, default=Status.PENDING
    )  # Payment status
    type = models.IntegerField(choices=Type.choices)

    def mark_as_paid(self):
        """Marks payment as completed."""
        with transaction.atomic():
            self.status = self.Status.PAID
            self.save()

    @staticmethod
    def create_stripe_checkout(
        request, borrowing, payment_type, total_amount
    ):
        """
        Creates a Stripe Checkout Session and returns its URL and session ID.
        """
        with transaction.atomic():
            if (
                payment_type == Payment.Type.FINE
            ):
                title = "Library borrowing fine"
            else:
                title = "Library borrowing payment"

            # Create Stripe Checkout Session
            stripe.api_key = settings.STRIPE_SECRET_KEY

            user_email = borrowing.user.email

            success_url = (
                request.build_absolute_uri(reverse("payment:stripe-success"))
                + "?session_id={CHECKOUT_SESSION_ID}"
            )
            cancel_url = request.build_absolute_uri(reverse("payment:stripe-cancel"))

            checkout_session = stripe.checkout.Session.create(
                customer_email=user_email,
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": f"{title}",
                            },
                            "unit_amount": int(total_amount),  # Stripe works in cents
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
            )

            # Create Payment record
            Payment.objects.create(
                borrowing=borrowing,
                session_id=checkout_session.id,
                session_url=checkout_session.url,
                amount_of_money=total_amount,
                status=Payment.Status.PENDING,
                type=payment_type,
            )

            return checkout_session.url

    def __str__(self):
        return f"Payment for Borrowing {self.borrowing.id}: {self.get_type_display()} - {self.get_status_display()} (${self.amount_of_money / 100})"
