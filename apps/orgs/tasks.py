from apps.orgs.models import FyleCredential


def async_update_fyle_credentials(fyle_org_id: str, refresh_token: str):
    fyle_credentials = FyleCredential.objects.filter(workspace__org_id=fyle_org_id).first()
    if fyle_credentials:
        fyle_credentials.refresh_token = refresh_token
        fyle_credentials.save()
