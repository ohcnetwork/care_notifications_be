from celery import shared_task

from booking_notifications.tasks.common import dispatch, get_booking
from booking_notifications.utils.types import EventType, ResourceType


@shared_task
def send_reminder(booking_id: int):
    booking = get_booking(booking_id)
    if booking is None:
        return
    if booking.status != "booked":
        return
    dispatch(booking, EventType.reminder, ResourceType.booking)
