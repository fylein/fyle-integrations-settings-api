from .api_base import ApiBase


class Employee(ApiBase):
    
    GET_EMPLOYEE_REPORT = '/v1/reports/custom?format=JSON&onlyCurrent=false'

    def sync_employees(self):
        """Get the list of employees from bambooHr
        Returns:
            List with dicts in Employee schema.
        """
        return self._post_request(self.GET_EMPLOYEE_REPORT)
