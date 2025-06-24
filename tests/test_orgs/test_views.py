import pytest
from django.urls import reverse
from rest_framework import status
from tests.helpers import dict_compare_keys
from apps.orgs.models import Org
from .mock_setup import mock_all_external_dependencies, mock_admin_employees


def test_ready_view_case_1(api_client, mocker, access_token, db):
    """
    Test the ready endpoint
    Case: returns 200 and correct message
    """
    url = reverse('ready')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    mock_dependencies = mock_all_external_dependencies(mocker)

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert dict_compare_keys(response.data, {'message': 'Ready'}) == [], 'Response data mismatch'


def test_orgs_get_view_case_1(api_client, mocker, access_token, db):
    """
    Test orgs GET view
    Case: returns 404 when org not found (expected behavior)
    """
    url = reverse('orgs')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    mock_dependencies = mock_all_external_dependencies(mocker)

    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_orgs_put_view_case_1(api_client, mocker, access_token, db):
    """
    Test orgs PUT view
    Case: creates/finds org based on Fyle admin response
    """
    url = reverse('orgs')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    mock_dependencies = mock_all_external_dependencies(mocker)

    data = {'name': 'Updated Org Name'}
    response = api_client.put(url, data, format='json')
    
    assert response.status_code == status.HTTP_200_OK

    # Verify org was created/found based on Fyle admin response (not the PUT data)
    org = Org.objects.filter(fyle_org_id='orHVw3ikkCxJ').first()
    assert org is not None
    assert org.name == 'Anagha Org'  # From actual Fyle admin response


def test_admin_view_case_1(api_client, mocker, access_token, db):
    """
    Test admin view
    Case: returns 200 for admin access
    """
    url = reverse('admin-view', kwargs={'org_id': 1})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    mock_dependencies = mock_all_external_dependencies(mocker)
    mock_admin_employees(mocker)

    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
