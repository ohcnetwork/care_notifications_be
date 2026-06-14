import logging

from care.utils import sms
from django.utils import timezone

from care_notifications.settings import plugin_settings
from care_notifications.common.types import EventType

logger = logging.getLogger(__name__)


_TEXT_SETTING = {
    EventType.booking_confirmation: "BOOKING_CONFIRMATION_SMS_TEXT",
    EventType.booking_reminder: "BOOKING_REMINDER_SMS_TEXT",
    EventType.booking_cancellation: "BOOKING_CANCEL_SMS_TEXT",
    EventType.booking_reschedule: "BOOKING_RESCHEDULED_SMS_TEXT",
}


def build_context(booking) -> dict:
    return {
        "patient_name": booking.patient.name,
        "slot_start": timezone.localtime(booking.token_slot.start_datetime),
    }


def send_sms(booking, event_type: EventType) -> bool:
    try:
        template = getattr(plugin_settings, _TEXT_SETTING[event_type])
        content = template.format(**build_context(booking))
        sms.send_text_message(
            content=content,
            recipients=[booking.patient.phone_number],
        )
        return True
    except Exception:
        logger.exception("SMS send failed for booking=%s", booking.id)
        return False
