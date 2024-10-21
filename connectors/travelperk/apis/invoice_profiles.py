"""
Travelperk Invoices
"""
from .api_base import ApiBase


class InvoiceProfiles(ApiBase):
    """Class for Invoice Profiles APIs."""

    GET_INVOICE_PROFILES = '/profiles'

    def get_all(self):
        """Get a list of the existing Invoice Profiles in the Organization.

        Returns:
            List with dicts in Invoice Profile schema.
        """
        return [*self.get_all_generator()]
    
    def get_all_generator(self):
        """
        Creates a generator that contains all profiles across all pages
        
        Parameters:
            object_type (str): The type of object to get
            api_url (str): The url for the wanted API
            params (dict): The parameters for the request

        Returns:
            Generator with all objects of type `object_type`
        """

        limit = 50
        params = {'limit': limit}
        total = self._get_request('total', InvoiceProfiles.GET_INVOICE_PROFILES, params=params)

        for offset in range(0, total, limit):
            params['offset'] = offset
            profiles = self._get_request('profiles', InvoiceProfiles.GET_INVOICE_PROFILES, params=params)
            for profile in profiles:
                yield profile
