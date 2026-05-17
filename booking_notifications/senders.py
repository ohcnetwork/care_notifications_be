import logging

from care.utils import sms
from care.utils.sms.utils import get_sms_content
from django.utils import timezone

from booking_notifications.utils.notification_type import NotificationType
from booking_notifications.settings import plugin_settings

logger = logging.getLogger(__name__)


_TEMPLATE_SETTING = {
    NotificationType.confirmation: "BOOKING_CONFIRMATION_SMS_TEMPLATE",
    NotificationType.reminder: "BOOKING_REMINDER_SMS_TEMPLATE",
    NotificationType.cancellation: "BOOKING_CANCEL_SMS_TEMPLATE",
    NotificationType.reschedule: "BOOKING_RESCHEDULED_SMS_TEMPLATE",
}


def build_context(booking) -> dict:
    return {
        "patient": booking.patient,
        "slot_start": timezone.localtime(booking.token_slot.start_datetime),
    }


def send_sms(booking, notif_type: NotificationType) -> bool:
    try:
        template_path = getattr(plugin_settings, _TEMPLATE_SETTING[notif_type])
        content = get_sms_content(template_path, build_context(booking))
        sms.send_text_message(
            content=content,
            recipients=[booking.patient.phone_number],
        )
        return True
    except Exception:
        logger.exception("SMS send failed for booking=%s", booking.id)
        return False
