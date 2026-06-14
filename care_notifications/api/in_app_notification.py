from care.emr.api.viewsets.base import (
    EMRBaseViewSet,
    EMRListMixin,
    EMRRetrieveMixin,
)
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from care_notifications.models.in_app_notification import InAppNotification
from care_notifications.resources.in_app_notification.spec import (
    InAppNotificationListSpec,
    InAppNotificationRetrieveSpec,
)


class InAppNotificationFilters(filters.FilterSet):
    event_type = filters.CharFilter(lookup_expr="iexact")
    resource_type = filters.CharFilter(lookup_expr="iexact")
    resource_id = filters.UUIDFilter()


class InAppNotificationViewSet(EMRListMixin, EMRRetrieveMixin, EMRBaseViewSet):
    database_model = InAppNotification
    pydantic_model = InAppNotificationListSpec
    pydantic_read_model = InAppNotificationListSpec
    pydantic_retrieve_model = InAppNotificationRetrieveSpec
    filterset_class = InAppNotificationFilters
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["created_date", "modified_date"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(recipient=self.request.user)
