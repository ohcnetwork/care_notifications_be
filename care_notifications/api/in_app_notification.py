from care.emr.api.viewsets.base import (
    EMRBaseViewSet,
    EMRListMixin,
    EMRRetrieveMixin,
)
from django.utils import timezone
from django_filters import rest_framework as filters
from pydantic import UUID4, BaseModel, Field
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from care_notifications.models.in_app_notification import InAppNotification
from care_notifications.resources.in_app_notification.spec import (
    InAppNotificationListSpec,
    InAppNotificationRetrieveSpec,
)


class InAppNotificationFilters(filters.FilterSet):
    event_type = filters.CharFilter(lookup_expr="iexact")
    resource_type = filters.CharFilter(lookup_expr="iexact")
    resource_id = filters.UUIDFilter()
    recipient = filters.UUIDFilter(field_name="recipient__external_id")
    unread = filters.BooleanFilter(field_name="read_at", lookup_expr="isnull")

class InAppNotificationMarkReadRequest(BaseModel):
    ids: list[UUID4] = Field(min_length=1)

class InAppNotificationViewSet(EMRListMixin, EMRRetrieveMixin, EMRBaseViewSet):
    database_model = InAppNotification
    pydantic_model = InAppNotificationListSpec
    pydantic_read_model = InAppNotificationListSpec
    pydantic_retrieve_model = InAppNotificationRetrieveSpec
    filterset_class = InAppNotificationFilters
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["created_date", "modified_date"]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["POST"])
    def mark_read(self, request, *args, **kwargs):
        payload = InAppNotificationMarkReadRequest.model_validate(request.data)
        updated = self.get_queryset().filter(external_id__in=payload.ids).update(read_at=timezone.now())
        return Response({"updated": updated})

    @action(detail=False, methods=["POST"])
    def mark_unread(self, request, *args, **kwargs):
        payload = InAppNotificationMarkReadRequest.model_validate(request.data)
        updated = self.get_queryset().filter(external_id__in=payload.ids).update(read_at=None)
        return Response({"updated": updated})
