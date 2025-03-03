from django.contrib.auth.mixins import LoginRequiredMixin
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from user.serializers import UserSerializer
import library_service.examples_swagger as swagger

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        examples=swagger.registration
    )
    def post(self, request, *args, **kwargs):
        """Register a new user."""
        return super().post(request, *args, **kwargs)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    @extend_schema(
        examples=swagger.my_profile_put_example
    )
    def put(self, request, *args, **kwargs):
        """Edit your profile"""
        return self.put(request, *args, **kwargs)

    @extend_schema(
        examples=swagger.my_profile_patch_example
    )
    def patch(self, request, *args, **kwargs):
        """Patch your profile"""
        return self.patch(request, *args, **kwargs)

class BindTelegram(APIView, LoginRequiredMixin): ...
