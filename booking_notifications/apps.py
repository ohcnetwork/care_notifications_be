from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

PLUGIN_NAME = "booking_notifications"


class BookingNotificationsConfig(AppConfig):
    name = PLUGIN_NAME
    verbose_name = _("Care Booking Notifications")

    def ready(self):
        import booking_notifications.signals  # noqa: F401
