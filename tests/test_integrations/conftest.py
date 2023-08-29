import pytest

from apps.integrations.models import Integration
from tests.test_integrations.fixture import post_integration_accounting, post_integration_hrms


@pytest.fixture()
def create_integrations():
    dummy_org_id = 'or3P3xJ0603e'
    Integration.objects.create(
        org_id=dummy_org_id,
        type=post_integration_accounting['type'],
        is_active=True,
        is_beta=True,
        tpa_id=post_integration_accounting['tpa_id'],
        tpa_name=post_integration_accounting['tpa_name']
    )
    Integration.objects.create(
        org_id=dummy_org_id,
        type=post_integration_hrms['type'],
        is_active=True,
        is_beta=True,
        tpa_id=post_integration_hrms['tpa_id'],
        tpa_name=post_integration_hrms['tpa_name']
    )
