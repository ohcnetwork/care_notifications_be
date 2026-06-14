from care.emr.models.location import FacilityLocationOrganization
from care.emr.models.organization import FacilityOrganizationUser
from care.users.models import User


def location_org_members(location):
    """Members of every FacilityOrganization that has access to this location."""
    if location is None:
        return User.objects.none()
    org_ids = FacilityLocationOrganization.objects.filter(
        location=location
    ).values_list("organization_id", flat=True)
    if not org_ids:
        return User.objects.none()
    user_ids = (
        FacilityOrganizationUser.objects.filter(organization_id__in=org_ids)
        .values_list("user_id", flat=True)
        .distinct()
    )
    return User.objects.filter(id__in=user_ids)
