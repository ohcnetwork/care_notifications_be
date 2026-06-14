from django.db import transaction

from care_notifications.models.outbound_notification import OutboundNotification
from care_notifications.settings import plugin_settings
from care_notifications.tasks import notify_rescheduled
from care_notifications.common.types import EventType, ResourceType


def handle_rescheduled(booking) -> None:
    if not OutboundNotification.objects.filter(
        resource_type=ResourceType.booking.value,
        resource_id=booking.external_id,
        event_type=EventType.booking_confirmation.value,
    ).exists():
        return

    if plugin_settings.BOOKING_NOTIFY_RESCHEDULED:
        transaction.on_commit(lambda: notify_rescheduled.delay(booking.id))
