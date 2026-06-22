from django.db import transaction

from care_notifications.settings import plugin_settings
from care_notifications.tasks import notify_diagnostic_report_ready


def handle_ready(diagnostic_report) -> None:
    if not plugin_settings.DIAGNOSTIC_REPORT_NOTIFY_READY:
        return
    transaction.on_commit(lambda: notify_diagnostic_report_ready.delay(diagnostic_report.id))
