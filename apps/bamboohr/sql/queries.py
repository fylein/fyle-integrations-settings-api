EMPLOYEE_DETAILS_QUERY = """
    select
    emp.displayName as 'EmployeeName',
    emp.workEmail as 'EmployeeEmail',
    emp.jobTitle as 'JobTitle',
    emp.location as 'Location',
    emp.department as 'DepartmentName',
    emp.mobilePhone as 'Mobile',
    emp.supervisorEmail as 'supervisorEmail',
    emp.status as 'status'
    from
    employeesnew emp where emp.status = 'Active' and EmployeeEmail is not null order by emp.displayName;
"""

EMPLOYEE_EMAIL_NOT_NULL = """
    select
    displayName
    from
    employeesnew where status='Active' and workEmail is NULL;
"""