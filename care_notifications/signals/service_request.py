from care.emr.models.service_request import ServiceRequest
from care.emr.resources.service_request.spec import ServiceRequestStatusChoices
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from care_notifications.handlers.service_request.raised import handle_raised
from care_notifications.settings import plugin_settings


@receiver(pre_save, sender=ServiceRequest)
def capture_status(sender, instance: ServiceRequest, **kwargs):
    if not plugin_settings.SERVICE_REQUEST_NOTIFICATIONS_ENABLED:
        return

    if not instance.pk:
        instance._previous_status = None
        return
    try:
        instance._previous_status = sender.objects.only("status").get(pk=instance.pk).status
    except sender.DoesNotExist:
        instance._previous_status = None


@receiver(post_save, sender=ServiceRequest)
def handle_notification(sender, instance: ServiceRequest, created: bool, **kwargs):
    if not plugin_settings.SERVICE_REQUEST_NOTIFICATIONS_ENABLED:
        return

    new_status = instance.status
    old_status = getattr(instance, "_previous_status", None)

    active = ServiceRequestStatusChoices.active.value
    if new_status != active or old_status == active:
        return

    handle_raised(instance)
