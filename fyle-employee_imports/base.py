class FyleEmployeeImport():

    def __init__(self, org_id: int):
        self.org_id = org_id
    
    def sync_fyle_employees(self):
        pass

    def get_existing_departments_from_fyle(self):
        pass

    def create_fyle_department_payload(self):
        pass

    def departments_to_be_imported(self):
        pass

    def post_department(self):
        pass

    def import_departments(self):
        pass

    def get_employee_and_approver_payload(self):
        pass

    def import_employees(self):
        pass

    def sync_hrms_employees(self):
        raise NotImplementedError('Implement sync_hrms_employees() in the child class')
    
    def sync_employees(self):
        pass

