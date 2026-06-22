from rest_framework.routers import DefaultRouter

from care_notifications.api.in_app_notification import InAppNotificationViewSet
from care_notifications.api.outbound_notification import OutboundNotificationViewSet

router = DefaultRouter()
router.register(
    r"in_app_notifications",
    InAppNotificationViewSet,
    basename="in_app_notifications",
)
router.register(
    r"outbound_notifications",
    OutboundNotificationViewSet,
    basename="outbound_notifications",
)

urlpatterns = router.urls
