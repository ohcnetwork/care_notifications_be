from django.db import transaction

from booking_notifications.models.notification import BookingNotification
from booking_notifications.settings import plugin_settings
from booking_notifications.tasks import notify_confirmation


def handle_confirmed(booking) -> None:
    BookingNotification.objects.get_or_create(booking=booking)

    if plugin_settings.BOOKING_NOTIFY_CONFIRMATION:
        transaction.on_commit(lambda: notify_confirmation.delay(booking.id))
