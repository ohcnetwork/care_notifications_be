from care.emr.models.scheduling.booking import TokenBooking
from care.emr.resources.scheduling.slot.spec import BookingStatusChoices
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from care_notifications.handlers.booking.cancelled import handle_cancelled
from care_notifications.handlers.booking.confirmed import handle_confirmed
from care_notifications.handlers.booking.rescheduled import handle_rescheduled
from care_notifications.settings import plugin_settings


@receiver(pre_save, sender=TokenBooking)
def capture_status(sender, instance: TokenBooking, **kwargs):
    if not plugin_settings.TOKEN_BOOKING_NOTIFICATIONS_ENABLED:
        return

    if not instance.pk:
        instance._previous_status = None
        return
    try:
        instance._previous_status = sender.objects.only("status").get(pk=instance.pk).status
    except sender.DoesNotExist:
        instance._previous_status = None


@receiver(post_save, sender=TokenBooking)
def handle_notification(sender, instance: TokenBooking, created: bool, **kwargs):
    if not plugin_settings.TOKEN_BOOKING_NOTIFICATIONS_ENABLED:
        return

    new_status = instance.status
    old_status = getattr(instance, "_previous_status", None)

    if created and new_status == BookingStatusChoices.booked.value:
        handle_confirmed(instance)
        return

    if old_status == new_status:
        return

    if new_status == BookingStatusChoices.booked.value and old_status in {
        BookingStatusChoices.pending.value,
        BookingStatusChoices.proposed.value,
        BookingStatusChoices.waitlist.value,
        None,
    }:
        handle_confirmed(instance)
    elif new_status == BookingStatusChoices.rescheduled.value:
        handle_rescheduled(instance)
    elif new_status == BookingStatusChoices.cancelled.value:
        handle_cancelled(instance)
