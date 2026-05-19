from django.db import transaction

from booking_notifications.models.notification import Notification
from booking_notifications.settings import plugin_settings
from booking_notifications.tasks import notify_rescheduled
from booking_notifications.utils.types import EventType, ResourceType


def handle_rescheduled(booking) -> None:
    if not Notification.objects.filter(
        resource_type=ResourceType.booking.value,
        resource_id=booking.external_id,
        event_type=EventType.confirmation.value,
    ).exists():
        return

    if plugin_settings.BOOKING_NOTIFY_RESCHEDULED:
        transaction.on_commit(lambda: notify_rescheduled.delay(booking.id))
