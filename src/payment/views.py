from datetime import datetime, date

import stripe
from django.conf import settings
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from borrowing.serializers import BorrowingReturnSerializer
from notification.signals import notification
from payment.models import Payment
from payment.serializers import EmptySerializer, PaymentSerializer


class StripeSuccessAPI(APIView):
    """
    Verifies successful payment using session_id.
    """
    permission_classes = (AllowAny,)
    serializer_class = EmptySerializer

    @transaction.atomic
    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        session_id = request.GET.get("session_id")
        if not session_id:
            return Response(
                {"error": "Session ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == "paid":
                # Retrieve payment record by session_id
                payment = Payment.objects.filter(session_id=session_id).first()
                if not payment:
                    return Response(
                        {"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND
                    )

                payment.mark_as_paid()  # Updates payment and ticket statuses

                if payment.type == Payment.Type.PAYMENT:
                    notification.send(
                        sender=self.__class__,
                        chat_id=settings.ADMIN_CHAT_ID,
                        message=(
                            f"✅ Payment successful!\n"
                            f"👤 User: {payment.borrowing.user}\n"
                            f"📚 Book: {payment.borrowing.book}\n"
                            f"💸 Amount: {payment.amount_of_money} USD\n"
                            f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                        )
                    )
                    return Response(
                        {
                            "message": "Payment successful",
                            "borrowing_id": payment.borrowing.id,
                        }
                    )
                else:
                    today = date.today()
                    serializer = BorrowingReturnSerializer(
                        payment.borrowing,
                        data={"actual_return_date": today},
                        partial=True,
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    payment.borrowing.book.inventory += 1
                    payment.borrowing.book.save()
                    return Response(
                        {
                            "message": f"Fine payment for borrowing {payment.borrowing.id} successful",
                            "borrowing_id": payment.borrowing.id,
                        }
                    )

            return Response(
                {"error": "Payment not completed"}, status=status.HTTP_400_BAD_REQUEST
            )

        except stripe.error.StripeError as e:
            return Response(
                {"error": f"Stripe error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST
            )


class StripeCancelAPI(APIView):
    """
    Handles cases where the user cancels the payment.
    """

    serializer_class = EmptySerializer

    def get(self, request):
        user = request.user
        payment = Payment.objects.get(
            borrowing__user=user, status=Payment.Status.PENDING
        )
        cancel_url = request.build_absolute_uri(
            reverse("payment:payment-cancel", kwargs={"pk": payment.id})
        )

        return Response(
            {
                "message": "Payment wasn't successful. You can try again.",
                "redirect_url": payment.session_url,
                "another_message": "Or cancel this payment:",
                "cancel_url": cancel_url
            }
        )


class PaymentViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Payment.objects.all().select_related()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(borrowing__user=self.request.user)

    @action(detail=True, methods=["POST"], url_path="renew")
    @transaction.atomic
    def renew_payment(self, request, pk=None):
        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

        if payment.status == Payment.Status.PENDING:
            return Response({"redirect_url": payment.session_url}, status=status.HTTP_200_OK)
        elif payment.status == Payment.Status.PAID:
            return Response({"error": "This payments is already paid"}, status=status.HTTP_400_BAD_REQUEST)

        if payment.type != Payment.Type.FINE:
            return Response({"error": "Cannot create new payment, borrowing does not exist anymore as payment expired. Please create new borrowing!"}, status=status.HTTP_400_BAD_REQUEST)
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {"name": str(payment.borrowing.book)},
                            "unit_amount": int(payment.amount_of_money * 100),
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=(request.build_absolute_uri(reverse("payment:stripe-success"))
                        + "?session_id={CHECKOUT_SESSION_ID}"),
                cancel_url = request.build_absolute_uri(reverse("payment:stripe-cancel"))
            )

            payment.session_id = session.id
            payment.session_url = session.url
            payment.status = Payment.Status.PENDING
            payment.save()
            return Response({"redirect_url": session.url}, status=status.HTTP_201_CREATED)
        except stripe.error.StripeError as e:
            return Response({"error": f"Stripe error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary="Retrieve payment details")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(summary="List all payments")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CancelPaymentAPIView(APIView):
    """
    A separate view for canceling a pending payment.
    """
    serializer_class = EmptySerializer

    def get(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

        if payment.status != Payment.Status.PENDING:
            return Response({"error": "Only pending payments can be canceled."},
                            status=status.HTTP_400_BAD_REQUEST)

        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            stripe.checkout.Session.expire(payment.session_id)
        except stripe.error.StripeError as e:
            return Response({"error": f"Stripe error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        payment.status = Payment.Status.EXPIRED
        payment.save()

        return Response({"message": f"Payment {payment.id} has been successfully canceled."},
                        status=status.HTTP_200_OK)