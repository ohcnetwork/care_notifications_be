import datetime
from typing import Any

from care.emr.resources.base import EMRResource
from care.emr.resources.user.spec import UserSpec
from pydantic import UUID4

from care_notifications.models.in_app_notification import InAppNotification


class InAppNotificationSpecBase(EMRResource):
    __model__ = InAppNotification
    __exclude__ = ["recipient"]

    id: UUID4 | None = None
    event_type: str
    resource_type: str
    resource_id: UUID4
    facility_id: UUID4 | None = None
    title: str
    body: str = ""
    payload: dict[str, Any] = {}
    read_at: datetime.datetime | None = None


class InAppNotificationListSpec(InAppNotificationSpecBase):
    created_date: datetime.datetime
    modified_date: datetime.datetime
    recipient: dict | None = None

    @classmethod
    def perform_extra_serialization(cls, mapping, obj, *args, **kwargs):
        mapping["id"] = obj.external_id
        if obj.recipient_id:
            mapping["recipient"] = UserSpec.serialize(obj.recipient).to_json()


class InAppNotificationRetrieveSpec(InAppNotificationListSpec):
    pass
