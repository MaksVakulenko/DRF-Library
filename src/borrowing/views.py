import datetime

from django.db import transaction
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingReturnSerializer,
)
from payment.models import Payment

MULTIPLIER = 2


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        return BorrowingSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        methods=["POST"],
        detail=True,
        url_path="return",
    )
    def return_book(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date is not None:
            return Response(
                {"This book has already been returned"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        today = datetime.date.today()
        if today > borrowing.expected_return_date:
            days_expired = (today - borrowing.expected_return_date).days
            fine = int((borrowing.book.daily_fee * days_expired) * 100) * MULTIPLIER
            checkout_url = Payment.create_stripe_checkout(
                request=request,
                borrowing=borrowing,
                payment_type=Payment.Type.FINE,
                total_amount=fine,
            )
            return Response({"redirect_url": checkout_url}, status=status.HTTP_200_OK)

        serializer = BorrowingReturnSerializer(
            borrowing, data={"actual_return_date": today}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        borrowing.book.inventory += 1
        borrowing.book.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Creates a reservation and returns a `payment_url`.
        """
        # Validate request payload
        serializer = BorrowingSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        # Save reservation and tickets
        self.perform_create(serializer)
        borrowing = serializer.instance
        # reservation.refresh_from_db()
        return Response(
            {"redirect_url": borrowing.checkout_url}, status=status.HTTP_201_CREATED
        )
