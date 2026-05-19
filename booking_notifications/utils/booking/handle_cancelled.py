from django.db import transaction

from booking_notifications.models.notification import Notification
from booking_notifications.settings import plugin_settings
from booking_notifications.tasks import notify_cancel
from booking_notifications.utils.types import EventType, ResourceType


def handle_cancelled(booking) -> None:
    if not Notification.objects.filter(
        resource_type=ResourceType.booking.value,
        resource_id=booking.external_id,
        event_type=EventType.confirmation.value,
    ).exists():
        return

    if plugin_settings.BOOKING_NOTIFY_CANCEL:
        transaction.on_commit(lambda: notify_cancel.delay(booking.id))
