import datetime

from django.db import transaction
from rest_framework import serializers
from django.conf import settings

from borrowing.models import Borrowing
from book.serializers import BookDetailBorrowingSerializer
from notification.signals import notification
from payment.models import Payment


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
        Borrowing.validate_if_user_has_pending_payment(user.id)
        Borrowing.validate_expected_return_date(data["expected_return_date"])
        Borrowing.validate_book_inventory(data["book"])

        return data

    # def create(self, validated_data):
    #     book = validated_data["book"]
    #     book.inventory -= 1
    #     book.save()
    #     return super().create(validated_data)

    @transaction.atomic
    def create(self, validated_data):
        borrowing = super().create(validated_data)
        # Резервуємо книгу
        borrowing.book.inventory -= 1
        borrowing.book.save()
        checkout_url = Payment.create_stripe_checkout(
            request=self.context["request"],
            payment_type=Payment.Type.PAYMENT,
            borrowing=borrowing,
            total_amount=borrowing.total_price(),
        )
        notification.send(
            sender=self.context["request"],
            to_admin_chat=True,
            message=(
                f"✅ New borrowing created!\n"
                f"👤 User: {self.context['request'].user}\n"
                f"📚 Book: {validated_data.get('book')}\n"
                f"⏳ Waiting for payment\n"
                f"📅 Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
        )
        borrowing.checkout_url = checkout_url
        return borrowing


class BorrowingListSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()
    book = serializers.StringRelatedField()
    payments = serializers.StringRelatedField(many=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "is_active",
            "payments",
        )

    def get_is_active(self, obj):
        return obj.actual_return_date is None


class BorrowingDetailSerializer(BorrowingListSerializer):
    book = BookDetailBorrowingSerializer()


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("actual_return_date",)
