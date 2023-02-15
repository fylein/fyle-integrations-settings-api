import pytest

from workato.exceptions import *
from apps.orgs.models import Org
from apps.bamboohr.models import BambooHr
from apps.orgs.actions import handle_managed_user_exception

@pytest.mark.django_db(databases=['default'])
def test_handle_managed_user_exception(mocker):
    
    mocker.patch(
        'workato.workato.ManagedUser.get_by_id',
        return_value={'id': 123}
    )
    
    mocker.patch(
        'workato.workato.Folders.get',
        return_value={'result': [{'id': 1234}]}
    )

    handle_managed_user_exception(10)
    org = Org.objects.get(id=10)
    bamboo = BambooHr.objects.get(org_id=10)


    assert org.managed_user_id == '123'
    assert bamboo.folder_id == '1234'
