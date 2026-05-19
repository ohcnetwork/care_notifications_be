from datetime import timedelta

from care.emr.models.scheduling.booking import TokenBooking
from celery import shared_task
from django.utils import timezone

from booking_notifications.settings import plugin_settings
from booking_notifications.tasks.send_reminder import send_reminder
from booking_notifications.utils.types import EventType, ResourceType


@shared_task
def sweep_reminders():
    if not plugin_settings.BOOKING_NOTIFY_REMINDER:
        return 0

    now = timezone.now()
    lead_cutoff = now + timedelta(minutes=int(plugin_settings.BOOKING_REMINDER_LEAD_MINUTES))

    due_ids = (
        TokenBooking.objects.filter(
            status="booked",
            token_slot__start_datetime__gt=now,
            token_slot__start_datetime__lte=lead_cutoff,
        )
        .exclude(
            notifications__resource_type=ResourceType.booking.value,
            notifications__event_type=EventType.reminder.value,
        )
        .values_list("id", flat=True)
    )

    count = 0
    for booking_id in due_ids:
        send_reminder.apply_async(args=[booking_id], expires=300)
        count += 1
    return count
