import pytest
from apps.orgs.models import Org, FyleCredential

@pytest.mark.django_db
def test_org_and_credential_creation():
    org = Org.objects.create(name='Test Org', fyle_org_id='org123', cluster_domain='https://test.com')
    cred = FyleCredential.objects.create(org=org, refresh_token='token123')
    assert cred.org == org
    assert Org.objects.count() == 1
    assert FyleCredential.objects.count() == 1
