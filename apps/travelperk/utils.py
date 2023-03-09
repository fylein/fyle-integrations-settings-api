from io import FileIO
from datetime import datetime, timezone
import uuid
import jwt


def get_signed_api_key(managed_user_id: str) -> str:
    """
    Sign the API key.
    """
    secret_file: FileIO = open('private.key', 'r')
    api_key: str = "secret key"
    customer_id: str = managed_user_id
    sub_params: str = ':'.join([api_key, str(customer_id)])
    encoded_token: str = jwt.encode(
        {
            'sub': sub_params,
            'jti': uuid.uuid4().hex,
            'origin': None,
            "iat": datetime.now(tz=timezone.utc)
        }, 
        secret_file.read(), 
        algorithm='RS256'
    )
    return encoded_token