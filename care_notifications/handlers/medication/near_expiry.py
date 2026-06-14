from care_notifications.settings import plugin_settings
from care_notifications.tasks import notify_medication_near_expiry


def handle_near_expiry(inventory_item_id: int) -> None:
    if not plugin_settings.MEDICATION_NOTIFY_NEAR_EXPIRY:
        return
    notify_medication_near_expiry.apply_async(args=[inventory_item_id], expires=3600)
