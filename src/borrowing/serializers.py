import datetime

from django.db import transaction
from rest_framework import serializers
from django.conf import settings

from borrowing.models import Borrowing
from book.serializers import BookDetailBorrowingSerializer
from notification.signals import notification
from payment.models import Payment
from library_service.settings import FINE_MULTIPLIER


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
    fine = serializers.SerializerMethodField()
    user = serializers.EmailField(source="user.email")

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "user",
            "expected_return_date",
            "actual_return_date",
            "book",
            "is_active",
            "fine",
            "payments",
        )

    def get_is_active(self, obj):
        return obj.actual_return_date is None

    def get_fine(self, obj):
        today = datetime.date.today()
        if self.get_is_active(obj) and today > obj.expected_return_date:
            days_expired = (today - obj.expected_return_date).days
            fine = (obj.book.daily_fee * days_expired) * FINE_MULTIPLIER
            return f"${fine}"
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        today = datetime.date.today()
        if not (self.get_is_active(instance) and today > instance.expected_return_date):
            data.pop("fine", None)
        return data


class BorrowingDetailSerializer(BorrowingListSerializer):
    book = BookDetailBorrowingSerializer()


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("actual_return_date",)
