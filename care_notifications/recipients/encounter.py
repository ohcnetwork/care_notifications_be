from care.emr.models.organization import FacilityOrganizationUser
from care.users.models import User


def care_team_members(encounter):
    if not encounter.care_team_users:
        return User.objects.none()
    return User.objects.filter(id__in=encounter.care_team_users)


def encounter_org_members(encounter):
    if not encounter.facility_organization_cache:
        return User.objects.none()
    user_ids = (
        FacilityOrganizationUser.objects.filter(
            organization_id__in=encounter.facility_organization_cache
        )
        .values_list("user_id", flat=True)
        .distinct()
    )
    return User.objects.filter(id__in=user_ids)


def care_team_and_encounter_orgs(encounter):
    """care_team_users + members of every org in facility_organization_cache."""
    ids = set(encounter.care_team_users or [])
    if encounter.facility_organization_cache:
        ids.update(
            FacilityOrganizationUser.objects.filter(
                organization_id__in=encounter.facility_organization_cache
            ).values_list("user_id", flat=True)
        )
    if not ids:
        return User.objects.none()
    return User.objects.filter(id__in=ids)
