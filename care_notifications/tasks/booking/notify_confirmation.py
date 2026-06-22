from celery import shared_task

from care_notifications.common.types import EventType, ResourceType
from care_notifications.tasks.common import dispatch, get_booking


@shared_task(autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 60})
def notify_confirmation(booking_id: int):
    booking = get_booking(booking_id)
    if booking is None:
        return
    dispatch(booking, EventType.booking_confirmation, ResourceType.booking)
