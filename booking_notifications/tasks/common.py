from care.emr.models.scheduling.booking import TokenBooking
from care.utils.models.base import BaseModel

from booking_notifications.models.notification import Notification
from booking_notifications.senders import send_sms
from booking_notifications.utils.types import EventType, ResourceType


def get_booking(booking_id: int):
    try:
        return TokenBooking.objects.select_related("patient", "token_slot").get(id=booking_id)
    except TokenBooking.DoesNotExist:
        return None


def dispatch(
    resource: BaseModel,
    event_type: EventType,
    resource_type: ResourceType,
) -> bool:
    notif = Notification.objects.create(
        resource_type=resource_type.value,
        resource_id=resource.external_id,
        event_type=event_type.value,
    )

    if not send_sms(resource, event_type):
        notif.delete()
        raise RuntimeError(
            f"SMS dispatch failed for resource={resource.external_id} event={event_type.value}"
        )
    return True

