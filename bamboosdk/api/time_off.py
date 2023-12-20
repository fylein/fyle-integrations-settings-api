from .api_base import ApiBase

class TimeOff(ApiBase):
	CHECK_URL = '/v1/meta/time_off/types/'
	
	def get(self):
		"""
			Get method to get the different fields, 
			used here for checking connection.
			Returns:
		"""
		return self._get_request(self.CHECK_URL)
