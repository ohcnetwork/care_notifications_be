import datetime

from care.emr.resources.base import EMRResource
from pydantic import UUID4

from care_notifications.models.web_push_subscription import WebPushSubscription


class WebPushSubscriptionListSpec(EMRResource):
    __model__ = WebPushSubscription

    id: UUID4 | None = None
    endpoint: str
    created_date: datetime.datetime

    @classmethod
    def perform_extra_serialization(cls, mapping, obj, *args, **kwargs):
        mapping["id"] = obj.external_id
