from .api.employee import Employee

class BambooHrSDK:

    def __init__(self, api_token, sub_domain):
        self.__api_token = api_token
        self.__sub_domain = sub_domain
            
        self.employees = Employee()
        self.employees.set_api_token(self.__api_token)
        self.employees.set_sub_domain(self.__sub_domain)
