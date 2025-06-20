import pytest
from apps.orgs.serializers import OrgSerializer
from apps.orgs.models import Org, User

@pytest.mark.django_db
def test_org_serializer_update_existing(mocker):
    org = Org.objects.create(name='Test Org', fyle_org_id='org123', cluster_domain='https://test.com')
    user = User.objects.create(user_id='user123', email='test@example.com')
    context = {'request': mocker.Mock(user=user.user_id, META={'HTTP_AUTHORIZATION': 'Bearer token'})}
    mocker.patch('apps.orgs.serializers.get_fyle_admin', return_value={
        'data': {'org': {'name': 'Test Org', 'id': 'org123'}, 'user_id': user.user_id}
    })
    serializer = OrgSerializer(instance=org, context=context)
    updated_org = serializer.update(org, {})
    assert user in updated_org.user.all() 
