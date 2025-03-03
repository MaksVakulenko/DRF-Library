from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Flushes all data and then seeds the database"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("⚠️ WARNING: This will delete all data!"))

        # Flush database (remove all data but keep schema)
        self.stdout.write("🔄 Flushing database...")
        call_command("flush", "--noinput")
        self.stdout.write(self.style.SUCCESS("✅ Database flushed successfully."))

        # Seed the database
        self.stdout.write("🌱 Seeding database...")
        call_command("seed_db")
        self.stdout.write(self.style.SUCCESS("🚀 Database reset and seeded successfully!"))
