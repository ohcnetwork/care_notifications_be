from django.db import transaction

from care_notifications.settings import plugin_settings
from care_notifications.tasks import notify_encounter_ip_created


def handle_ip_created(encounter) -> None:
    if not plugin_settings.ENCOUNTER_NOTIFY_IP_CREATED:
        return
    transaction.on_commit(lambda: notify_encounter_ip_created.delay(encounter.id))
