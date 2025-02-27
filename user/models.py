from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Roles(models.TextChoices):
        LIBRARIAN = "LIBRARIAN", _("Librarian")
        READER = "READER", _("Reader")
    username = None
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(
        max_length=10, choices=Roles, default=Roles.READER
    )
    chat_id = models.CharField(max_length=9, unique=True, null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if self.is_staff:
            self.role = self.Roles.LIBRARIAN
        else:
            self.role = self.Roles.READER
        super().save(*args, **kwargs)

    objects = UserManager()
