from .api.employee import Employee
from .api.webhook import Webhook
from .api.time_off import TimeOff

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
        self.webhook = Webhook()
        self.time_off = TimeOff()

        self.set_api_token()
        self.set_sub_domain()

    def set_api_token(self):
        """
            Set the api token for all the APIs
        """
        self.employees.set_api_token(self.__api_token)
        self.webhook.set_api_token(self.__api_token)
        self.time_off.set_api_token(self.__api_token)

    def set_sub_domain(self):
        """
            Set sub domain for all the APIs
        """
        self.employees.set_sub_domain(self.__sub_domain)
        self.webhook.set_sub_domain(self.__sub_domain)
        self.time_off.set_sub_domain(self.__sub_domain)
