from datetime import timedelta

from care.emr.models.scheduling.booking import TokenBooking
from celery import shared_task
from django.utils import timezone

from care_notifications.common.types import EventType, ResourceType
from care_notifications.models.outbound_notification import OutboundNotification
from care_notifications.settings import plugin_settings
from care_notifications.tasks.booking.send_reminder import send_reminder


@shared_task
def sweep_reminders():
    now = timezone.now()
    lead_cutoff = now + timedelta(minutes=int(plugin_settings.BOOKING_REMINDER_LEAD_MINUTES))

    already_notified = OutboundNotification.objects.filter(
        resource_type=ResourceType.booking.value,
        event_type=EventType.booking_reminder.value,
    ).values_list("resource_id", flat=True)

    due_ids = (
        TokenBooking.objects.filter(
            status="booked",
            token_slot__start_datetime__gt=now,
            token_slot__start_datetime__lte=lead_cutoff,
        )
        .exclude(external_id__in=already_notified)
        .values_list("id", flat=True)
    )

    count = 0
    for booking_id in due_ids:
        send_reminder.apply_async(args=[booking_id], expires=300)
        count += 1
    return count

