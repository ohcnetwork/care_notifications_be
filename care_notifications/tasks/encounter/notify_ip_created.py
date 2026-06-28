from care.emr.models.encounter import Encounter
from celery import shared_task

from care_notifications.common.types import EventType, ResourceType
from care_notifications.recipients.encounter import care_team_and_encounter_orgs
from care_notifications.settings import plugin_settings
from care_notifications.tasks.common import notify_users


@shared_task(autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 60})
def notify_encounter_ip_created(encounter_id: int):
    try:
        encounter = Encounter.objects.select_related("patient", "current_location").get(
            id=encounter_id
        )
    except Encounter.DoesNotExist:
        return

    recipients = care_team_and_encounter_orgs(encounter)

    context = {
        "patient_name": encounter.patient.name,
        "location_name": encounter.current_location.name if encounter.current_location else "",
    }
    title = plugin_settings.ENCOUNTER_IP_CREATED_TITLE.format(**context)
    body = plugin_settings.ENCOUNTER_IP_CREATED_BODY.format(**context)

    notify_users(
        recipients=recipients,
        event_type=EventType.encounter_ip_created.value,
        resource_type=ResourceType.encounter.value,
        resource_id=encounter.external_id,
        title=title,
        body=body,
    )
