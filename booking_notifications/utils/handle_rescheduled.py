from django.db import transaction

from booking_notifications.models.notification import BookingNotification
from booking_notifications.settings import plugin_settings
from booking_notifications.tasks import notify_rescheduled


def handle_rescheduled(booking) -> None:
    if not BookingNotification.objects.filter(booking=booking).exists():
        return

    if plugin_settings.BOOKING_NOTIFY_RESCHEDULED:
        transaction.on_commit(lambda: notify_rescheduled.delay(booking.id))
