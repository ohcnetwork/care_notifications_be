from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

PLUGIN_NAME = "care_notifications"


class CareNotificationsConfig(AppConfig):
    name = PLUGIN_NAME
    verbose_name = _("Care Notifications")

    def ready(self):
        import care_notifications.authorization  # noqa: F401
        import care_notifications.signals  # noqa: F401
        from care.security.permissions.base import PermissionController

        from care_notifications.permissions import NotificationPermissions

        PermissionController.register_permission_handler(NotificationPermissions)
