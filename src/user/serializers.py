from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from user.services import send_verification_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "first_name", "last_name", "password")
        read_only_fields = ("id",)
        required_fields = ("email", "password")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8,
                "style": {"input_type": "password"},
            }
        }

    @transaction.atomic
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        send_verification_email(user)
        return user

    @transaction.atomic
    def update(self, instance, validated_data, partial=True):
        password = validated_data.pop("password", None)
        email = validated_data.pop("email", None)

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        if email:
            user.email = email
            user.is_active = False
            user.save()
            send_verification_email(user)

        return user
