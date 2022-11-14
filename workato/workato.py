"""
Workato Connector Module
"""
import os
import jwt
from io import FileIO
from datetime import datetime, timezone
import uuid

from .apis import *


class Workato:
    """
    Workato Connector
    """

    def __init__(self):
        """
        Initialize connection to Workato
        """

        self.connections = Connections()
        self.recipes = Recipes()
        self.managed_users = ManagedUser()
        self.properties = Properties()
        self.folders = Folders()
        self.packages = Packages()

    def _get_signed_api_key(self, managed_user_id: str) -> str:
        """
        Sign the API key.
        """
        secret_file: FileIO = open('./secrets/private.key', 'r')
        api_key: str = os.environ.get('WK_API_KEY')
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
