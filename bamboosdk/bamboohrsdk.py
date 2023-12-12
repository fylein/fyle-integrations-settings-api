from .api.employee import Employee

class BambooHrSDK:
    """
    Creates connection with BambooHr APIs

    Parameters:
        api_token (str): API token for BambooHr
        sub_domain (str): Sub domain of the user in BambooHr
    """

    def __init__(self, api_token: str, sub_domain: str):
        self.__api_token = api_token
        self.__sub_domain = sub_domain
            
        self.employees = Employee()
        self.employees.set_api_token(self.__api_token)
        self.employees.set_sub_domain(self.__sub_domain)
