import pytest

from apps.integrations.actions import get_integration

from .fixture import post_integration_hrms


@pytest.mark.django_db(databases=['default'])
def test_get_integration(mocker, access_token, create_integrations):
    dummy_org_id = 'or3P3xJ0603e'
    mocker.patch(
        'apps.integrations.actions.get_org_id_from_access_token',
        return_value=dummy_org_id
    )
    mocker.patch(
        'apps.integrations.actions.get_cluster_domain',
        return_value='https://hehe.fyle.tech'
    )

    integration = get_integration('HRMS', access_token).first()

    assert integration.org_id == dummy_org_id
    assert integration.tpa_id == post_integration_hrms['tpa_id']
    assert integration.tpa_name == post_integration_hrms['tpa_name']
    assert integration.type == post_integration_hrms['type']
    assert integration.is_active == post_integration_hrms['is_active']
    assert integration.is_beta == True
    assert integration.disconnected_at == None
