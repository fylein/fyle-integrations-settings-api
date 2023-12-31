import uuid
from datetime import datetime, timezone
from fyle.platform import Platform

import jwt
from apps.orgs.models import FyleCredential
from apps.orgs.exceptions import handle_workato_exception
from django.conf import settings


@handle_workato_exception(task_name='Get Signed API Key')
def get_signed_api_key(managed_user_id: str) -> str:
    """
    Sign the API key.
    """
    secret_file = settings.WK_JWT_PRIVATE_KEY
    api_key: str = settings.WK_API_KEY
    customer_id: str = managed_user_id
    sub_params: str = ':'.join([api_key, str(customer_id)])
    encoded_token: str = jwt.encode(
        {
            'sub': sub_params,
            'jti': uuid.uuid4().hex,
            'origin': None,
            "iat": datetime.now(tz=timezone.utc)
        }, 
        secret_file, 
        algorithm='RS256'
    )

    return encoded_token


def create_fyle_connection(org_id: str):
    """
    Create a Fyle connection using the provided credentials.

    Returns:
        FyleSDK: An instance of the FyleSDK class for making API requests.
    """

    fyle_credentials = FyleCredential.objects.get(org_id=org_id)

    base_url = settings.FYLE_BASE_URL
    client_id = settings.FYLE_CLIENT_ID
    client_secret = settings.FYLE_CLIENT_SECRET
    refresh_token = fyle_credentials.refresh_token
    token_url = settings.FYLE_TOKEN_URI

    connection = Platform(
        server_url=base_url,
        token_url=token_url,
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token
    )

    return connection
