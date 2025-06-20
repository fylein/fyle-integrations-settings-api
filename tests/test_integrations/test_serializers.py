import pytest
from datetime import datetime
from apps.integrations.serializers import IntegrationSerializer
from apps.integrations.models import Integration

@pytest.mark.django_db
def test_integration_serializer_inactive_branch():
    # Create an active integration first
    integration = Integration.objects.create(
        org_id='test_org_id',
        org_name='Test Org',
        type='test_integration',
        tpa_id='test_tpa_id',
        tpa_name='Test TPA',
        is_active=True
    )
    data = {
        'org_id': 'test_org_id',
        'org_name': 'Test Org',
        'type': 'test_integration',
        'tpa_id': 'test_tpa_id',
        'tpa_name': 'Test TPA',
        'is_active': False
    }
    serializer = IntegrationSerializer()
    updated_integration = serializer.create(data)
    assert updated_integration.is_active is False
    assert updated_integration.disconnected_at is not None
    assert isinstance(updated_integration.disconnected_at, datetime)
