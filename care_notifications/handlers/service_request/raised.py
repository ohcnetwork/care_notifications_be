from django.db import transaction

from care_notifications.settings import plugin_settings
from care_notifications.tasks import notify_service_request_raised


def handle_raised(service_request) -> None:
    if not plugin_settings.SERVICE_REQUEST_NOTIFY_RAISED:
        return
    if service_request.healthcare_service_id is None:
        return
    transaction.on_commit(lambda: notify_service_request_raised.delay(service_request.id))
