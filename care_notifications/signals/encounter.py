from care.emr.models.encounter import Encounter
from care.emr.resources.encounter.constants import ClassChoices
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from care_notifications.handlers.encounter.ip_created import handle_ip_created
from care_notifications.settings import plugin_settings


@receiver(pre_save, sender=Encounter)
def capture_state(sender, instance: Encounter, **kwargs):
    if not plugin_settings.ENCOUNTER_NOTIFICATIONS_ENABLED:
        return

    if not instance.pk:
        instance._previous_encounter_class = None
        instance._previous_current_location_id = None
        return
    try:
        previous = sender.objects.only("encounter_class", "current_location_id").get(
            pk=instance.pk
        )
        instance._previous_encounter_class = previous.encounter_class
        instance._previous_current_location_id = previous.current_location_id
    except sender.DoesNotExist:
        instance._previous_encounter_class = None
        instance._previous_current_location_id = None


@receiver(post_save, sender=Encounter)
def handle_notification(sender, instance: Encounter, created: bool, **kwargs):
    if not plugin_settings.ENCOUNTER_NOTIFICATIONS_ENABLED:
        return

    new_class = instance.encounter_class
    new_location_id = instance.current_location_id
    old_class = getattr(instance, "_previous_encounter_class", None)
    old_location_id = getattr(instance, "_previous_current_location_id", None)

    imp = ClassChoices.imp.value
    now_ip_with_location = (new_class == imp) and (new_location_id is not None)
    was_ip_with_location = (old_class == imp) and (old_location_id is not None)

    if now_ip_with_location and not was_ip_with_location:
        handle_ip_created(instance)
