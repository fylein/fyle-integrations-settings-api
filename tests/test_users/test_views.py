import json
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from tests.fixture import fixture

User = get_user_model()


def test_profile_view_case_1(mock_dependencies, api_client, access_token):
    """
    Test profile view
    Case: Returns 200 with correct user and org data
    """
    url = reverse('profile')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert response_data['data']['org']['id'] == 'orHVw3ikkCxJ'
    assert response_data['data']['user_id'] == 'usqywo0f3nBY'
