from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

from user.services import send_verification_email
from user.tasks import send_verification_email_task

User = get_user_model()


class BaseUserTest(APITestCase):
    """Base class for user-related tests."""

    def setUp(self):
        """Creates a test user."""
        self.user = User.objects.create_user(
            email="user@example.com", password="testpass123"
        )
        self.client.force_authenticate(self.user)
        self.user.save()


class UserAPITest(BaseUserTest):
    """Tests for user API endpoints."""

    @patch("user.tasks.send_verification_email_task.delay")
    def test_register_user(self, mock_celery_task):
        """Checks successful user registration."""
        data = {"email": "newuser@example.com", "password": "testpass123"}
        response = self.client.post(reverse("user:create"), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())
        mock_celery_task.assert_called_once()

    def test_login_user(self):
        """Checks successful user login."""
        self.user.is_active = True
        self.user.save()

        data = {"email": "user@example.com", "password": "testpass123"}
        response = self.client.post(reverse("user:token_obtain_pair"), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_update_user_profile(self):
        """Checks profile update via PATCH."""
        data = {"first_name": "NewName", "last_name": "NewLastName"}
        response = self.client.patch(reverse("user:manage"), data)

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, "NewName")
        self.assertEqual(self.user.last_name, "NewLastName")

    def test_change_password(self):
        """Checks password change via PATCH."""
        data = {"password": "newpass123"}
        response = self.client.patch(reverse("user:manage"), data)

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password("newpass123"))


class VerifyEmailTest(BaseUserTest):
    """Tests for email verification."""

    def setUp(self):
        super().setUp()
        self.user.is_active = False
        self.user.save()

    def test_verify_email(self):
        """Checks if user is activated after email verification."""
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        url = reverse("user:verify_email", kwargs={"uidb64": uid, "token": token})
        response = self.client.get(url)

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.is_active)


class EmailServiceTest(BaseUserTest):
    """Tests for email verification service."""

    def setUp(self):
        super().setUp()
        self.user.is_active = False
        self.user.save()

    @patch("user.tasks.send_verification_email_task.delay")
    def test_send_verification_email_task_called(self, mock_celery_task):
        """Ensures `send_verification_email_task.delay` is called when `send_verification_email` is executed."""
        send_verification_email(self.user)
        mock_celery_task.assert_called_once()


class CeleryTaskTest(APITestCase):
    """Tests for Celery email task."""

    @patch("user.tasks.send_mail")
    def test_send_verification_email_task(self, mock_send_mail):
        """Ensures `send_mail` is called correctly."""
        subject = "Test Subject"
        message = "Test Message"
        recipient = ["test@example.com"]
        from_email = settings.DEFAULT_FROM_EMAIL

        send_verification_email_task.run(subject, message, recipient)

        mock_send_mail.assert_called_once_with(subject, message, from_email, recipient)
