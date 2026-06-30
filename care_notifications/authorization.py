from care.emr.models.organization import FacilityOrganizationUser, OrganizationUser
from care.security.authorization import AuthorizationController
from care.security.authorization.base import AuthorizationHandler

from care_notifications.permissions import NotificationPermissions


class NotificationAccess(AuthorizationHandler):
    def can_list_all_notifications(self, user):
        if user.is_superuser:
            return True
        roles = self.get_role_from_permissions(
            [NotificationPermissions.can_list_all_notifications.name]
        )
        return (
            OrganizationUser.objects.filter(user=user, role_id__in=roles).exists()
            or FacilityOrganizationUser.objects.filter(
                user=user, role_id__in=roles
            ).exists()
        )


AuthorizationController.register_override_controller(NotificationAccess)
