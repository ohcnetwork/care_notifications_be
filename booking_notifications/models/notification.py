from care.utils.models.base import BaseModel
from django.db import models


class Notification(BaseModel):
    resource_type = models.CharField(max_length=32)
    resource_id = models.UUIDField()
    event_type = models.CharField(max_length=32)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=("resource_type", "resource_id")),
        ]

