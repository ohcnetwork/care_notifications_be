from celery import shared_task
from django.utils import timezone

from booking_notifications.models.notification import BookingNotification
from booking_notifications.tasks.common import NotificationType, dispatch, get_booking


@shared_task(autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 60})
def notify_cancel(booking_id: int):
    booking = get_booking(booking_id)
    if booking is None:
        return

    notif, _ = BookingNotification.objects.get_or_create(booking=booking)

    if notif.cancel_sent_at is not None:
        return

    if dispatch(booking, NotificationType.cancellation):
        notif.cancel_sent_at = timezone.now()
        notif.save()
