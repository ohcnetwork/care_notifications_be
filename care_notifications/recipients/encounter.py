from care.emr.models.encounter import EncounterOrganization
from care.emr.models.organization import FacilityOrganizationUser
from care.users.models import User


def care_team_members(encounter):
    if not encounter.care_team_users:
        return User.objects.none()
    return User.objects.filter(id__in=encounter.care_team_users)


def encounter_org_members(encounter):
    org_ids = EncounterOrganization.objects.filter(encounter=encounter).values("organization_id")
    user_ids = (
        FacilityOrganizationUser.objects.filter(organization_id__in=org_ids)
        .values_list("user_id", flat=True)
        .distinct()
    )
    return User.objects.filter(id__in=user_ids)


def care_team_and_encounter_orgs(encounter):
    """care_team_users + members of orgs explicitly attached to this encounter.
    """
    ids = set(encounter.care_team_users or [])
    org_ids = list(
        EncounterOrganization.objects.filter(encounter=encounter).values_list(
            "organization_id", flat=True
        )
    )
    if org_ids:
        ids.update(
            FacilityOrganizationUser.objects.filter(organization_id__in=org_ids)
            .values_list("user_id", flat=True)
        )
    if not ids:
        return User.objects.none()
    return User.objects.filter(id__in=ids)
