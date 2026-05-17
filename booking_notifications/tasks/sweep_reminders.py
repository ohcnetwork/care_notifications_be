from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from booking_notifications.models.notification import BookingNotification
from booking_notifications.settings import plugin_settings
from booking_notifications.tasks.send_reminder import send_reminder


@shared_task
def sweep_reminders():
    if not plugin_settings.BOOKING_NOTIFY_REMINDER:
        return 0

    now = timezone.now()
    lead_cutoff = now + timedelta(minutes=int(plugin_settings.BOOKING_REMINDER_LEAD_MINUTES))

    due_ids = BookingNotification.objects.filter(
        reminder_sent_at__isnull=True,
        booking__status="booked",
        booking__token_slot__start_datetime__gt=now,
        booking__token_slot__start_datetime__lte=lead_cutoff,
    ).values_list("booking_id", flat=True)

    count = 0
    for booking_id in due_ids:
        send_reminder.apply_async(args=[booking_id], expires=300)
        count += 1
    return count
