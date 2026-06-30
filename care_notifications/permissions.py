import enum

from care.security.permissions.constants import Permission, PermissionContext
from care.security.roles.role import ADMIN_ROLE, ADMINISTRATOR, FACILITY_ADMIN_ROLE


class NotificationPermissions(enum.Enum):
    can_list_all_notifications = Permission(
        "Can list all notifications",
        "List in-app and web-push notifications for every user, not just one's own.",
        PermissionContext.GENERIC,
        [ADMINISTRATOR, ADMIN_ROLE, FACILITY_ADMIN_ROLE],
    )
