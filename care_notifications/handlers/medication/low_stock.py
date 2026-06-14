from care_notifications.settings import plugin_settings
from care_notifications.tasks import notify_medication_low_stock


def handle_low_stock(inventory_item_id: int) -> None:
    if not plugin_settings.MEDICATION_NOTIFY_LOW_STOCK:
        return
    notify_medication_low_stock.apply_async(args=[inventory_item_id], expires=3600)
