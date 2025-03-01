import datetime

import stripe
from django.conf import settings
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from borrowing.serializers import BorrowingReturnSerializer
from payment.models import Payment
from payment.serializers import EmptySerializer


class StripeSuccessAPI(APIView):
    """
    Verifies successful payment using session_id.
    """
    serializer_class = EmptySerializer

    @transaction.atomic
    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        session_id = request.GET.get("session_id")
        if not session_id:
            return Response({"error": "Session ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == "paid":
                # Retrieve payment record by session_id
                payment = Payment.objects.filter(session_id=session_id).first()
                if not payment:
                    return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)


                payment.mark_as_paid()  # Updates payment and ticket statuses

                if payment.type == Payment.Type.PAYMENT:
                    payment.borrowing.book.inventory -= 1
                    payment.borrowing.book.save()
                    return Response({"message": "Payment successful", "borrowing_id": payment.borrowing.id})
                else:
                    today = datetime.date.today()
                    serializer = BorrowingReturnSerializer(payment.borrowing, data={"actual_return_date": today}, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    payment.borrowing.book.inventory += 1
                    payment.borrowing.book.save()
                    return Response({"message": f"Fine payment for borrowing {payment.borrowing.id} successful", "borrowing_id": payment.borrowing.id})

            return Response({"error": "Payment not completed"}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            return Response({"error": f"Stripe error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class StripeCancelAPI(APIView):
    """
    Handles cases where the user cancels the payment.
    """
    serializer_class = EmptySerializer

    def get(self, request):
        return Response({"message": "Payment was cancelled. You can try again."})
