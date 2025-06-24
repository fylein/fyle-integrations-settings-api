import json

import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from tests.fixture import fixture
from rest_framework import status
from tests.test_users.mock_setup import mock_requests_shared_mock

User = get_user_model()


def test_profile_view(api_client, mocker, access_token, db):
    """
    Test profile view
    """
    url = reverse('profile')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    mock_requests, mock_response = mock_requests_shared_mock(mocker)
    mock_response.status_code = 200
    mock_response.text = '{"data": {"user": {"email": "test@example.com"}}}'

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    response = json.loads(response.content)

    assert response['data']['org']['id'] == 'orHVw3ikkCxJ'
    assert response['data']['user_id'] == 'usqywo0f3nBY'
