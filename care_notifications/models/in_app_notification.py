from care.utils.models.base import BaseModel
from django.conf import settings
from django.db import models


class InAppNotification(BaseModel):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="in_app_notifications",
    )
    event_type = models.CharField(max_length=128)
    resource_type = models.CharField(max_length=32)
    resource_id = models.UUIDField()
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    payload = models.JSONField(default=dict, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
