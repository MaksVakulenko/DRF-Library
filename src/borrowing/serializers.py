from rest_framework import serializers

from borrowing.models import Borrowing
from book.serializers import BookSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "expected_return_date",
            "book",
        )

    def validate(self, data):
        data = super().validate(data)

        user = self.context["request"].user

        Borrowing.validate_if_user_has_borrowing(user.id)
        Borrowing.validate_expected_return_date(data["expected_date"])
        Borrowing.validate_book_inventory(data["book"].inventory)

        return data


class BorrowingListSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()
    book = serializers.CharField(source="book.title")

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "is_active",
        )

    def get_is_active(self, obj):
        return obj.actual_return_date is None


class BorrowingDetailSerializer(BorrowingListSerializer):
    book = BookSerializer()
