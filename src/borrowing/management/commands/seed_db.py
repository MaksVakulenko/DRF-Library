from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import OperationalError

from book.models import Book, Author
from borrowing.models import Borrowing
from payment.models import Payment


class Command(BaseCommand):
    help = "Fills the database with realistic test data"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        try:
            # Check if any data exists in the database
            if (
                    User.objects.exists() or
                    Payment.objects.exists() or
                    Borrowing.objects.exists() or
                    Book.objects.exists() or
                    Author.objects.exists()
            ):
                self.stdout.write(
                    self.style.ERROR("❌  Database is not empty! Please save existing data and clear it from db before seeding."))
                self.stdout.write(
                    self.style.WARNING("💡 Use `python manage.py flush --noinput` to clear data or `reset_db` to renovate."))
                return  # Stop execution if data exists

        except OperationalError:
            self.stdout.write(self.style.ERROR("❌ Database is not available. Did you run `migrate`?"))
            return

        self.stdout.write("📥 Loading data from fixture...")
        try:
            call_command("loaddata", "initial_data.json")  # Load your fixture file
            self.stdout.write(self.style.SUCCESS("Fixture data loaded successfully."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading fixture: {e}"))

