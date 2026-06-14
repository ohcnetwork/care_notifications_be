import datetime

from care.emr.resources.base import EMRResource
from pydantic import UUID4

from care_notifications.models.outbound_notification import OutboundNotification


class OutboundNotificationSpecBase(EMRResource):
    __model__ = OutboundNotification

    id: UUID4 | None = None
    event_type: str
    resource_type: str
    resource_id: UUID4
    sent_at: datetime.datetime


class OutboundNotificationListSpec(OutboundNotificationSpecBase):
    created_date: datetime.datetime

    @classmethod
    def perform_extra_serialization(cls, mapping, obj, *args, **kwargs):
        mapping["id"] = obj.external_id
