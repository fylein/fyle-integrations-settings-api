from .api_base import ApiBase
from datetime import datetime

class Employee(ApiBase):
    
    GET_EMPLOYEE_REPORT = '/v1/reports/custom?format=JSON&onlyCurrent=false'
    GET_EMPLOYEE = '/v1/employees/{}/?fields=workEmail&onlyCurrent=false'
    payload = { "fields": ["displayName", "firstName", "lastName", "department", "workEmail", "supervisorEmail", "status"] }

    def get_all(self, schedule: bool, sync_employee_from: datetime = None):
        """Get the list of employees from bambooHr
        Returns:
            List with dicts in Employee schema.
        """

        if schedule:
            self.payload['filters'] = { "lastChanged": {
            "includeNull": "yes",
            "value": str(sync_employee_from)
        }}
        return self._post_request(self.GET_EMPLOYEE_REPORT, payload=self.payload)

    def get(self, id):
        return self._get_request(self.GET_EMPLOYEE.format(id))
