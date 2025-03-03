from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = "notification"

    def ready(self):
        from . import signals, receivers # noqa
