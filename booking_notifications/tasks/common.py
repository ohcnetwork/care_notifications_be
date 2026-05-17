from care.emr.models.scheduling.booking import TokenBooking

from booking_notifications.utils.notification_type import NotificationType
from booking_notifications.senders import send_sms


def get_booking(booking_id: int):
    try:
        return TokenBooking.objects.select_related("patient", "token_slot").get(id=booking_id)
    except TokenBooking.DoesNotExist:
        return None


def dispatch(booking: TokenBooking, notification_type: NotificationType):
    return send_sms(booking, notification_type)
