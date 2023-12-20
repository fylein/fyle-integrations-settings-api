from .base import FyleEmployeeImport
from bamboosdk.bamboohrsdk import BambooHrSDK
from apps.bamboohr.models import BambooHr


class BambooHrEmployeeImport(FyleEmployeeImport):

    def __init__(self, org_id: int):
        super().__init__(org_id)
        bamboo_hr = BambooHr.objects.get(org_id__in= org_id)
        self.bamboohr_sdk = BambooHrSDK(api_token=bamboo_hr.api_token, sub_domain=bamboo_hr.sub_domain)

    def sync_employees(self):
        pass

    def upsert_employees(self):
        pass
