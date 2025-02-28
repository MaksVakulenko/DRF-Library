import datetime

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingReturnSerializer
)


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
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
        url_path="return-book",
    )
    def return_book(self, request, pk=None):
        borrowing = self.get_object()
        today = datetime.date.today()

        serializer = BorrowingReturnSerializer(borrowing, data={"actual_return_date": today}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        borrowing.book.inventory += 1
        borrowing.book.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
