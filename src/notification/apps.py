from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = "notification"

    def ready(self):
        print("Notification app ready")
        from . import signals, receivers # noqa
