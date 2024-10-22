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
        """Create a generator with all the existing Invoice Profiles in the Organization.

        Returns:
            Generator with dicts in Invoice Profile schema.
        """
        return self._get_all_generator('profiles', self.GET_INVOICE_PROFILES)