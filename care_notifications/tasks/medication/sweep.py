from datetime import timedelta
from decimal import Decimal

from care.emr.models.inventory_item import InventoryItem
from care.emr.resources.inventory.product_knowledge.spec import ProductTypeOptions
from celery import shared_task
from django.utils import timezone

from care_notifications.common.types import EventType
from care_notifications.handlers.medication.low_stock import handle_low_stock
from care_notifications.handlers.medication.near_expiry import handle_near_expiry
from care_notifications.models.in_app_notification import InAppNotification
from care_notifications.settings import plugin_settings


@shared_task
def sweep_medication_stock():
    """Scan medication InventoryItems and fire near-expiry / low-stock events.
    """
    if not plugin_settings.MEDICATION_NOTIFICATIONS_ENABLED:
        return {"near_expiry": 0, "low_stock": 0}

    counts = {"near_expiry": 0, "low_stock": 0}
    medication = ProductTypeOptions.medication.value

    if plugin_settings.MEDICATION_NOTIFY_NEAR_EXPIRY:
        lead_days = int(plugin_settings.MEDICATION_NEAR_EXPIRY_LEAD_DAYS)
        now = timezone.now()
        cutoff = now + timedelta(days=lead_days)
        already_notified = InAppNotification.objects.filter(
            event_type=EventType.medication_stock_near_expiry.value,
        ).values_list("resource_id", flat=True)
        due_ids = (
            InventoryItem.objects.filter(
                product__expiration_date__gte=now,
                product__expiration_date__lte=cutoff,
                product__product_knowledge__product_type=medication,
                net_content__gt=0,
            )
            .exclude(external_id__in=already_notified)
            .values_list("id", flat=True)
        )
        for item_id in due_ids:
            handle_near_expiry(item_id)
            counts["near_expiry"] += 1

    if plugin_settings.MEDICATION_NOTIFY_LOW_STOCK:
        threshold = Decimal(str(plugin_settings.MEDICATION_LOW_STOCK_THRESHOLD))
        already_notified = InAppNotification.objects.filter(
            event_type=EventType.medication_stock_low.value,
        ).values_list("resource_id", flat=True)
        due_ids = (
            InventoryItem.objects.filter(
                net_content__lt=threshold,
                product__product_knowledge__product_type=medication,
            )
            .exclude(external_id__in=already_notified)
            .values_list("id", flat=True)
        )
        for item_id in due_ids:
            handle_low_stock(item_id)
            counts["low_stock"] += 1

    return counts
