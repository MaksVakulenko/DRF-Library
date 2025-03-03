import os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_service.settings")
django.setup()

from telegram_bot.main import bot


if __name__ == "__main__":
    bot.polling()