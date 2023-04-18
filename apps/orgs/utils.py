import uuid
from datetime import datetime, timezone

import jwt
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
