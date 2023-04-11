import pytest

from workato.exceptions import *
from apps.orgs.models import Org
from apps.bamboohr.models import BambooHr
from apps.orgs.actions import handle_managed_user_exception

@pytest.mark.django_db(databases=['default'])
def test_handle_managed_user_exception(mocker, access_token, get_org_id, get_bamboohr_id):
    
    mocker.patch(
        'workato.workato.ManagedUser.get_by_id',
        return_value={'id': 123}
    )
    
    mocker.patch(
        'workato.workato.Folders.get',
        return_value={'result': [{'id': 1234}]}
    )

    org = Org.objects.get(id=get_org_id)
    handle_managed_user_exception(org)
    
    org = Org.objects.get(id=get_org_id)
    bamboo = BambooHr.objects.filter(org=org).first()


    assert org.managed_user_id == '123'
    assert bamboo.folder_id == '1234'
