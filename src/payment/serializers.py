from rest_framework import serializers

from payment.models import Payment


class EmptySerializer(serializers.Serializer):
    """Empty serializer for API views that do not require serialization."""
    pass


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payment details."""

    class Meta:
        model = Payment
        fields = ("id", "borrowing", "session_url", "session_id", "amount_of_money", "status", "type")
        read_only_fields = ("id", "session_url", "session_id", "amount_of_money", "status", "type")
