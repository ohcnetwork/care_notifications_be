from care.emr.models.scheduling.booking import TokenBooking
from care.utils.models.base import BaseModel

from care_notifications.channels.inapp import dispatch_inapp
from care_notifications.channels.sms import send_sms
from care_notifications.channels.webpush import dispatch_webpush
from care_notifications.common.types import EventType, ResourceType
from care_notifications.models.outbound_notification import OutboundNotification
from care_notifications.settings import plugin_settings


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


def notify_users(
    *,
    recipients,
    event_type: str,
    resource_type: str,
    resource_id,
    title: str,
    body: str = "",
    facility_id=None,
    payload: dict | None = None,
) -> None:
    recipients = list(recipients)
    dispatch_inapp(
        recipients=recipients,
        event_type=event_type,
        resource_type=resource_type,
        resource_id=resource_id,
        title=title,
        body=body,
        facility_id=facility_id,
        payload=payload,
    )
    if plugin_settings.WEBPUSH_NOTIFICATIONS_ENABLED:
        dispatch_webpush(
            recipients=recipients,
            title=title,
            body=body,
            payload={
                "event_type": event_type,
                "resource_type": resource_type,
                "resource_id": str(resource_id),
                "facility_id": str(facility_id) if facility_id else None,
                **(payload or {}),
            },
        )
