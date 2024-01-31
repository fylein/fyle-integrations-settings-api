from fyle.platform import Platform

from apps.orgs.models import FyleCredential
from django.conf import settings


def create_fyle_connection(org_id: str):
    """
    Create a Fyle connection using the provided credentials.

    Returns:
        FyleSDK: An instance of the FyleSDK class for making API requests.
    """

    fyle_credentials = FyleCredential.objects.get(org_id=org_id)

    client_id = settings.FYLE_CLIENT_ID
    client_secret = settings.FYLE_CLIENT_SECRET
    refresh_token = fyle_credentials.refresh_token
    token_url = settings.FYLE_TOKEN_URI

    server_url = '{}/platform/v1beta'.format(fyle_credentials.org.cluster_domain)

    connection = Platform(
        server_url=server_url,
        token_url=token_url,
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token
    )

    return connection
