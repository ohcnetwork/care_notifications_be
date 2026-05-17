from celery import shared_task
from django.utils import timezone

from booking_notifications.models.notification import BookingNotification
from booking_notifications.utils.notification_type import NotificationType
from booking_notifications.tasks.common import dispatch, get_booking


@shared_task
def send_reminder(booking_id: int):
    booking = get_booking(booking_id)
    if booking is None:
        return
    if booking.status != "booked":
        return
    state, _ = BookingNotification.objects.get_or_create(booking=booking)
    if state.reminder_sent_at is not None:
        return
    if dispatch(booking, NotificationType.reminder):
        state.reminder_sent_at = timezone.now()
        state.save()
