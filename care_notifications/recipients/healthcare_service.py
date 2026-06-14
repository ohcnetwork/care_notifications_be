from care.emr.models.organization import FacilityOrganizationUser
from care.users.models import User


def managing_org_members(healthcare_service):
    if healthcare_service is None or healthcare_service.managing_organization_id is None:
        return User.objects.none()
    user_ids = (
        FacilityOrganizationUser.objects.filter(
            organization_id=healthcare_service.managing_organization_id
        )
        .values_list("user_id", flat=True)
        .distinct()
    )
    return User.objects.filter(id__in=user_ids)
