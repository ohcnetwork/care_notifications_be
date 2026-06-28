from care.emr.models.inventory_item import InventoryItem
from celery import shared_task

from care_notifications.common.types import EventType, ResourceType
from care_notifications.recipients.location import location_org_members
from care_notifications.settings import plugin_settings
from care_notifications.tasks.common import notify_users


@shared_task(autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 60})
def notify_medication_near_expiry(inventory_item_id: int):
    try:
        item = InventoryItem.objects.select_related(
            "location", "product", "product__product_knowledge"
        ).get(id=inventory_item_id)
    except InventoryItem.DoesNotExist:
        return

    recipients = location_org_members(item.location)
    expiration = item.product.expiration_date

    context = {
        "product_name": item.product.product_knowledge.name,
        "expiration_date": expiration.strftime("%d %b %Y") if expiration else "",
        "location_name": item.location.name,
        "net_content": item.net_content,
    }
    title = plugin_settings.MEDICATION_NEAR_EXPIRY_TITLE.format(**context)
    body = plugin_settings.MEDICATION_NEAR_EXPIRY_BODY.format(**context)

    notify_users(
        recipients=recipients,
        event_type=EventType.medication_stock_near_expiry.value,
        resource_type=ResourceType.medication_stock.value,
        resource_id=item.external_id,
        title=title,
        body=body,
    )
