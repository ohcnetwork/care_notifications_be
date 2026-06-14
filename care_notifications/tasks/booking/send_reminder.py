from celery import shared_task

from care_notifications.common.types import EventType, ResourceType
from care_notifications.tasks.common import dispatch, get_booking


@shared_task
def send_reminder(booking_id: int):
    booking = get_booking(booking_id)
    if booking is None:
        return
    if booking.status != "booked":
        return
    dispatch(booking, EventType.booking_reminder, ResourceType.booking)
