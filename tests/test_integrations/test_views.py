import json

from apps.integrations.models import Integration
import pytest
from django.urls import reverse
from .fixture import post_integration_accounting, post_integration_accounting_2, post_integration_hrms, patch_integration_no_tpa_name, patch_integration, patch_integration_invalid_tpa_name, patch_integration_partial


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_post_accounting(api_client, mocker, access_token):
    """Test POST of Integrations and GET ordering by updated_at."""
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id":dummy_org_id, "name":"Dummy Org"}
    )
    mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.post(url, post_integration_accounting)
    assert response.status_code == 201
    data = response.json()
    assert data['org_id'] == dummy_org_id
    assert data['tpa_id'] == post_integration_accounting['tpa_id']
    assert data['tpa_name'] == post_integration_accounting['tpa_name']
    assert data['type'] == post_integration_accounting['type']
    assert data['is_active'] == post_integration_accounting['is_active']
    assert data['is_beta'] is True
    assert data['disconnected_at'] is None
    api_client.post(url, post_integration_accounting_2)
    api_client.post(url, post_integration_hrms)
    response = api_client.get(url)
    data = response.json()
    assert data[0]['type'] == 'ACCOUNTING'
    assert data[1]['type'] == 'HRMS'
    assert data[0]['updated_at'] < data[1]['updated_at']


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_post(api_client, mocker, access_token):
    """Test POST of Integrations and update on duplicate POST."""
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id":dummy_org_id, "name":"Dummy Org"}
    )
    mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.post(url, post_integration_accounting)
    assert response.status_code == 201
    data = response.json()
    assert data['org_id'] == dummy_org_id
    assert data['tpa_id'] == post_integration_accounting['tpa_id']
    assert data['tpa_name'] == post_integration_accounting['tpa_name']
    assert data['type'] == post_integration_accounting['type']
    assert data['is_active'] == post_integration_accounting['is_active']
    assert data['is_beta'] is True
    assert data['disconnected_at'] is None
    accounting_integration_id = data['id']
    response = api_client.post(url, post_integration_hrms)
    assert response.status_code == 201
    data = response.json()
    assert data['org_id'] == dummy_org_id
    assert data['tpa_id'] == post_integration_hrms['tpa_id']
    assert data['tpa_name'] == post_integration_hrms['tpa_name']
    assert data['type'] == post_integration_hrms['type']
    assert data['is_active'] == post_integration_hrms['is_active']
    assert data['is_beta'] is True
    assert data['disconnected_at'] is None
    # A second POST with the same org_id and type should update the record
    response = api_client.post(url, post_integration_accounting_2)
    assert response.status_code == 201
    data = response.json()
    assert data['id'] == accounting_integration_id
    assert Integration.objects.filter(org_id=dummy_org_id).count() == 2
    assert data['org_id'] == dummy_org_id
    assert data['tpa_id'] == post_integration_accounting_2['tpa_id']
    assert data['tpa_name'] == post_integration_accounting_2['tpa_name']
    assert data['type'] == post_integration_accounting_2['type']
    assert data['is_active'] == post_integration_accounting_2['is_active']
    assert data['is_beta'] is True
    assert data['disconnected_at'] is None


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_get(api_client, mocker, access_token, create_integrations):
    """Test GET of Integrations and filtering by type."""
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id":dummy_org_id, "name":"Dummy Org"}
    )
    mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    response = api_client.get(url, {'type': 'ACCOUNTING'})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['org_id'] == dummy_org_id
    assert data[0]['tpa_id'] == post_integration_accounting['tpa_id']
    assert data[0]['tpa_name'] == post_integration_accounting['tpa_name']
    assert data[0]['type'] == post_integration_accounting['type']
    assert data[0]['is_active'] == post_integration_accounting['is_active']
    assert data[0]['is_beta'] is True
    assert data[0]['disconnected_at'] is None
    response = api_client.get(url, {'type': 'HRMS'})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['org_id'] == dummy_org_id
    assert data[0]['tpa_id'] == post_integration_hrms['tpa_id']
    assert data[0]['tpa_name'] == post_integration_hrms['tpa_name']
    assert data[0]['type'] == post_integration_hrms['type']
    assert data[0]['is_active'] == post_integration_hrms['is_active']
    assert data[0]['is_beta'] is True
    assert data[0]['disconnected_at'] is None


@pytest.mark.parametrize("method", ["get", "post", "patch"])
@pytest.mark.django_db(databases=['default'])
def test_integrations_view_invalid_access_token(api_client, method):
    """Test GET/POST/PATCH with invalid access token returns 403 or 400 for POST."""
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ey.ey.ey')
    func = getattr(api_client, method)
    if method == "patch":
        resp = func(url, post_integration_accounting)
        assert resp.status_code == 403
    elif method == "post":
        resp = func(url)
        assert resp.status_code == 400
    else:
        resp = func(url)
        assert resp.status_code == 403


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_post_missing_fields(api_client, mocker, access_token):
    """Test POST with missing required fields returns 400."""
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id":dummy_org_id, "name":"Dummy Org"}
    )
    mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    # Remove tpa_id (required field)
    payload = dict(post_integration_accounting)
    payload.pop('tpa_id')
    response = api_client.post(url, payload)
    assert response.status_code == 400


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_patch_missing_tpa_name(api_client, mocker, access_token):
    """Test PATCH without tpa_name returns 400."""
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id":dummy_org_id, "name":"Dummy Org"}
    )
    mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.patch(url,  json.dumps(patch_integration_no_tpa_name), content_type="application/json")
    assert response.status_code == 400


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_patch_inactive_integration(api_client, mocker, access_token):
    """Test PATCH with non-existent/inactive integration returns correct message."""
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id":dummy_org_id, "name":"Dummy Org"}
    )
    mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.patch(url,  json.dumps(patch_integration_invalid_tpa_name), content_type="application/json")
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Integration is inactive or does not exist'


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_patch_error_handling(api_client, mocker, access_token):
    """Test PATCH error handling when super().patch raises Exception."""
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        return_value={"id":dummy_org_id, "name":"Dummy Org"}
    )
    mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )
    url = reverse('integrations:integrations')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    # Patch the view's patch method to raise Exception
    with mocker.patch('apps.integrations.views.IntegrationsView.patch', side_effect=Exception('Something went wrong')):
        resp = api_client.patch(url, json.dumps(patch_integration), content_type="application/json")
        assert resp.status_code == 500


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_get_invalid_token_custom(api_client, mocker):
    """Test GET with invalid token triggers AuthenticationFailed in get."""
    url = reverse('integrations:integrations')
    mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        side_effect=Exception('Invalid access token')
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer invalid')
    resp = api_client.get(url)
    assert resp.status_code == 403
    assert resp.data['detail'] == 'Invalid access token'


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_patch_invalid_token_custom(api_client, mocker):
    """Test PATCH with invalid token triggers AuthenticationFailed in patch."""
    url = reverse('integrations:integrations')
    mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        side_effect=Exception('Invalid access token')
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer invalid')
    resp = api_client.patch(url, {'tpa_name': 'foo'})
    assert resp.status_code == 403
    assert resp.data['detail'] == 'Invalid access token'


@pytest.mark.django_db(databases=['default'])
def test_integrations_view_post_invalid_token_custom(api_client, mocker):
    """Test POST with invalid token triggers AuthenticationFailed in perform_create."""
    url = reverse('integrations:integrations')
    mocker.patch(
        'apps.integrations.views.get_org_id_and_name_from_access_token',
        side_effect=Exception('Invalid access token')
    )
    api_client.credentials(HTTP_AUTHORIZATION='Bearer invalid')
    resp = api_client.post(url, {'type': 'ACCOUNTING', 'tpa_id': 'foo', 'tpa_name': 'bar', 'is_active': True})
    assert resp.status_code == 403
    assert resp.data['detail'] == 'Invalid access token'
