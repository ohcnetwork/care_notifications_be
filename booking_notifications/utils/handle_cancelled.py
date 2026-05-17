from django.db import transaction

from booking_notifications.models.notification import BookingNotification
from booking_notifications.settings import plugin_settings
from booking_notifications.tasks import notify_cancel


def handle_cancelled(booking) -> None:
    if not BookingNotification.objects.filter(booking=booking).exists():
        return

    if plugin_settings.BOOKING_NOTIFY_CANCEL:
        transaction.on_commit(lambda: notify_cancel.delay(booking.id))
