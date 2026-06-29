from care.emr.api.viewsets.base import (
    EMRBaseViewSet,
    EMRListMixin,
    EMRRetrieveMixin,
)
from care.security.authorization import AuthorizationController
from django.core.exceptions import PermissionDenied
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from care_notifications.models.outbound_notification import OutboundNotification
from care_notifications.resources.outbound_notification.spec import (
    OutboundNotificationListSpec,
)


class OutboundNotificationFilters(filters.FilterSet):
    event_type = filters.CharFilter(lookup_expr="iexact")
    resource_type = filters.CharFilter(lookup_expr="iexact")
    resource_id = filters.UUIDFilter()


class OutboundNotificationViewSet(EMRListMixin, EMRRetrieveMixin, EMRBaseViewSet):
    database_model = OutboundNotification
    pydantic_model = OutboundNotificationListSpec
    pydantic_read_model = OutboundNotificationListSpec
    pydantic_retrieve_model = OutboundNotificationListSpec
    filterset_class = OutboundNotificationFilters
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["created_date", "sent_at"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not AuthorizationController.call("can_list_all_notifications", self.request.user):
            raise PermissionDenied("You do not have permission to view these notifications")
        return queryset

