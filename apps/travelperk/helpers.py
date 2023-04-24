import json
import logging
import requests

from django.conf import settings

logger = logging.getLogger(__name__)
logger.level = logging.INFO


def get_refresh_token_using_auth_code(code: str):
    response = requests.post(
        url=settings.TRAVELPERK_TOKEN_URL,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': settings.TRAVELPERK_CLIENT_ID,
            'client_secret': settings.TRAVELPERK_CLIENT_SECRET,
            'redirect_uri': settings.TRAVELPERK_REDIRECT_URI
        }
    )

    print('response.text',response.text, type(response.text))
    api_response = json.loads(response.text)

    if response.status_code == 200:
        print(api_response)
        return api_response['refresh_token']
    else:
        raise Exception(api_response)
