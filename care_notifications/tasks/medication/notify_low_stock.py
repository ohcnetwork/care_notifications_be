from care.emr.models.inventory_item import InventoryItem
from celery import shared_task

from care_notifications.common.types import EventType, ResourceType
from care_notifications.recipients.location import location_org_members
from care_notifications.settings import plugin_settings
from care_notifications.tasks.common import notify_users


@shared_task(autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 60})
def notify_medication_low_stock(inventory_item_id: int):
    try:
        item = InventoryItem.objects.select_related(
            "location", "product", "product__product_knowledge"
        ).get(id=inventory_item_id)
    except InventoryItem.DoesNotExist:
        return

    recipients = location_org_members(item.location)

    context = {
        "product_name": item.product.product_knowledge.name,
        "net_content": item.net_content,
        "location_name": item.location.name,
    }
    title = plugin_settings.MEDICATION_LOW_STOCK_TITLE.format(**context)
    body = plugin_settings.MEDICATION_LOW_STOCK_BODY.format(**context)

    notify_users(
        recipients=recipients,
        event_type=EventType.medication_stock_low.value,
        resource_type=ResourceType.medication_stock.value,
        resource_id=item.external_id,
        title=title,
        body=body,
    )
