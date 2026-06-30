from care.emr.models.service_request import ServiceRequest
from celery import shared_task

from care_notifications.common.types import EventType, ResourceType
from care_notifications.recipients.healthcare_service import managing_org_members
from care_notifications.settings import plugin_settings
from care_notifications.tasks.common import notify_users


@shared_task(autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 60})
def notify_service_request_raised(service_request_id: int):
    try:
        service_request = ServiceRequest.objects.select_related(
            "healthcare_service", "patient", "facility"
        ).get(id=service_request_id)
    except ServiceRequest.DoesNotExist:
        return

    recipients = managing_org_members(service_request.healthcare_service)

    context = {
        "patient_name": service_request.patient.name,
        "service_request_title": service_request.title,
    }
    title = plugin_settings.SERVICE_REQUEST_RAISED_TITLE.format(**context)
    body = plugin_settings.SERVICE_REQUEST_RAISED_BODY.format(**context)

    notify_users(
        recipients=recipients,
        event_type=EventType.service_request_raised.value,
        resource_type=ResourceType.service_request.value,
        resource_id=service_request.external_id,
        title=title,
        body=body,
        facility_id=service_request.facility.external_id,
    )
