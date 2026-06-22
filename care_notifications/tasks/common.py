from care.emr.models.scheduling.booking import TokenBooking
from care.utils.models.base import BaseModel

from care_notifications.channels.sms import send_sms
from care_notifications.common.types import EventType, ResourceType
from care_notifications.models.outbound_notification import OutboundNotification


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
    notif = OutboundNotification.objects.create(
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

