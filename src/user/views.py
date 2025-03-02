from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class BindTelegram(APIView, LoginRequiredMixin): ...


class VerifyEmailView(APIView):
    """API view to verify user email via token."""

    def get(self, request, uidb64, token):
        """Handles email verification when the user clicks the link."""
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(get_user_model(), pk=uid)

            if user.is_active:
                return Response({"message": "Email already verified."}, status=status.HTTP_200_OK)

            if not default_token_generator.check_token(user, token):  # Validate the token
                return Response({"error": "Invalid or expired verification token."}, status=status.HTTP_400_BAD_REQUEST)

            # Activate user
            user.is_active = True
            user.save()

            return Response({"message": "Email successfully verified! You can now log in."}, status=status.HTTP_200_OK)

        except Exception:
            return Response({"error": "Invalid verification link."}, status=status.HTTP_400_BAD_REQUEST)
