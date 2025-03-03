from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from user.tasks import send_verification_email_task


def send_verification_email(user):
    """Generate verification link dynamically and send an email."""
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)  # Generate a secure token

    verification_url = f"{settings.FRONTEND_URL}/api/user/verify-email/{uid}/{token}/"

    subject = "Confirm Your Email"
    message = f"""
    Hi {user.first_name} {user.last_name},

    Welcome! Please confirm your email by clicking the link below:

    {verification_url}

    If you did not make this action, ignore this email.
    """

    send_verification_email_task.delay(subject, message, [user.email])  # Send via Celery
