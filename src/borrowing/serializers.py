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

        Borrowing.validate_if_user_has_expired_borrowing(user.id)
        Borrowing.validate_expected_return_date(data["expected_return_date"])
        Borrowing.validate_book_inventory(data["book"])

        return data

    def create(self, validated_data):
        book = validated_data["book"]
        book.inventory -= 1
        book.save()
        return super().create(validated_data)


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


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("actual_return_date",)
