from care_notifications.models.in_app_notification import InAppNotification


def dispatch_inapp(
    *,
    recipients,
    event_type: str,
    resource_type: str,
    resource_id,
    title: str,
    body: str = "",
    payload: dict | None = None,
) -> int:
    rows = [
        InAppNotification(
            recipient=user,
            event_type=event_type,
            resource_type=resource_type,
            resource_id=resource_id,
            title=title,
            body=body,
            payload=payload or {},
        )
        for user in recipients
    ]
    if not rows:
        return 0
    InAppNotification.objects.bulk_create(rows)
    return len(rows)
