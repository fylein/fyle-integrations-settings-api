from apps.bamboohr.models import BambooHr
from apps.fyle_hrms_mappings.models import DestinationAttribute
from fyle_employee_imports.bamboo_hr import BambooHrEmployeeImport
from apps.users.models import User

def refresh_employees(org_id: int, user: User):
    """
        Sync Employees from BambooHR to Fyle
    """
    bambooHrImporter = BambooHrEmployeeImport(org_id=org_id, user=user)
    bambooHrImporter.sync_employees()

