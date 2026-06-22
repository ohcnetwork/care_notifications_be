from care.emr.models.diagnostic_report import DiagnosticReport
from care.emr.resources.diagnostic_report.spec import DiagnosticReportStatusChoices
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from care_notifications.handlers.diagnostic_report.ready import handle_ready
from care_notifications.settings import plugin_settings


@receiver(pre_save, sender=DiagnosticReport)
def capture_status(sender, instance: DiagnosticReport, **kwargs):
    if not plugin_settings.DIAGNOSTIC_REPORT_NOTIFICATIONS_ENABLED:
        return

    if not instance.pk:
        instance._previous_status = None
        return
    try:
        instance._previous_status = sender.objects.only("status").get(pk=instance.pk).status
    except sender.DoesNotExist:
        instance._previous_status = None


@receiver(post_save, sender=DiagnosticReport)
def handle_notification(sender, instance: DiagnosticReport, created: bool, **kwargs):
    if not plugin_settings.DIAGNOSTIC_REPORT_NOTIFICATIONS_ENABLED:
        return

    new_status = instance.status
    old_status = getattr(instance, "_previous_status", None)

    final = DiagnosticReportStatusChoices.final.value
    if new_status != final or old_status == final:
        return

    handle_ready(instance)
