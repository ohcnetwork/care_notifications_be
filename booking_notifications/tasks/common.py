from care.emr.models.scheduling.booking import TokenBooking

from booking_notifications.models.notification import BookingNotification
from booking_notifications.senders import send_sms
from booking_notifications.utils.types import EventType, ResourceType


def get_booking(booking_id: int):
    try:
        return TokenBooking.objects.select_related("patient", "token_slot").get(id=booking_id)
    except TokenBooking.DoesNotExist:
        return None


def dispatch(
    booking: TokenBooking,
    event_type: EventType,
    resource_type: ResourceType,
) -> bool:
    notif = BookingNotification.objects.create(
        resource_type=resource_type.value,
        booking=booking,
        event_type=event_type.value,
    )

    if not send_sms(booking, event_type):
        notif.delete()
        raise RuntimeError(
            f"SMS dispatch failed for booking={booking.id} event={event_type.value}"
        )
    return True
