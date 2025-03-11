import datetime

from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from library_service.settings import FINE_MULTIPLIER
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingReturnSerializer,
)
from notification.signals import notification
from payment.models import Payment
import library_service.examples_swagger as swagger
from library_service.messages import get_message_book_returned


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
        """
        Allows admins to see borrowing records for specific user.
        Also allows user see their own borrowing records and
        filter them by active status of borrowing.
        """
        queryset = self.queryset

        if self.action == "list":
            queryset = self.queryset.select_related(
                'user',  # Select user from the related User model
                'book'  # Select book from the related Book model
            ).prefetch_related(
                'book__authors'  # Prefetch authors related to the book
            )

        if is_active := self.request.query_params.get("is_active"):
            queryset = queryset.filter(actual_return_date__isnull=is_active in ("True", "true", "1"))
        # Filtering for admins
        if self.request.user.is_staff:
            user_id = self.request.query_params.get("user_id")
            return queryset.filter(user__id=user_id) if user_id else queryset

        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        parameters=swagger.borrow_id_parameter,
        examples=swagger.borrowing_return_example
    )
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

        if borrowing.user != self.request.user:
            return Response(
                {"user": "You can't return not your borrowing"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        today = datetime.date.today()
        if today > borrowing.expected_return_date:
            days_expired = (today - borrowing.expected_return_date).days
            fine = int((borrowing.book.daily_fee * days_expired) * 100) * FINE_MULTIPLIER
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
        notification.send(
            sender=self.__class__,
            to_admin_chat=True,
            message=get_message_book_returned(borrowing)
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        examples=swagger.borrowing_post_example
    )
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Creates a borrowing and returns a `payment_url`.
        """
        # Validate request payload
        serializer = BorrowingSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        borrowing = serializer.instance
        return Response(
            {"redirect_url": borrowing.checkout_url}, status=status.HTTP_201_CREATED
        )

    @extend_schema(
        parameters=swagger.borrowing_filter_parameters
    )
    def list(self, request, *args, **kwargs):
        """List of borrowings."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        parameters=swagger.borrow_id_parameter
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a borrowing."""
        return super().retrieve(request, *args, **kwargs)
