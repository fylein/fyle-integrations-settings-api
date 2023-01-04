import sys
import polling

from workato import Workato
from apps.bamboohr.models import BambooHr
from apps.orgs.models import Org

workspace_ids = []
for org_id in workspace_ids:
    connector = Workato()

    try:
        org = Org.objects.filter(id=org_id).first()
        bamboohr = BambooHr.objects.filter(org_id=org_id).first()
        package = connector.packages.post(org.managed_user_id, bamboohr.folder_id, 'assets/bamboohr_package.zip')
        polling.poll(
            lambda: connector.packages.get(org.managed_user_id, package['id'])['status'] == 'completed',
            step=5,
            timeout=50
        )
        bamboohr.package_id = package['id']
        bamboohr.save()

    except Exception as exception:
        print('something wrong happened with org id - {}'.format(org_id), exception)
