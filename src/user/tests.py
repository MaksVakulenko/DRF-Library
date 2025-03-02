from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user.models import User


class UserAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("user:create")
        self.login_url = reverse("user:token_obtain_pair")
        self.me_url = reverse("user:manage")
        self.refresh_url = reverse("user:token_refresh")

        self.user_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User",
        }

    def test_create_user(self):
        """Create user"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.user_data["email"]).exists())

    def test_login_user(self):
        """GET token for user"""
        User.objects.create_user(**self.user_data)

        response = self.client.post(
            self.login_url,
            {"email": self.user_data["email"], "password": self.user_data["password"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_get_user_profile(self):
        """Get profile"""
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)

        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def test_update_user_profile(self):
        """Update profile"""
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)

        updated_data = {"first_name": "Updated"}
        response = self.client.patch(self.me_url, updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], updated_data["first_name"])

    def test_refresh_token(self):
        """Refresh token"""
        User.objects.create_user(**self.user_data)

        response = self.client.post(
            self.login_url,
            {"email": self.user_data["email"], "password": self.user_data["password"]},
        )
        refresh_token = response.data["refresh"]

        response = self.client.post(self.refresh_url, {"refresh": refresh_token})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
