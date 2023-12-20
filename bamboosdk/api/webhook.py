from .api_base import ApiBase


class Webhook(ApiBase):
    """ Class for webhook APIs for bamboohr """

    POST_WEBHOOK = '/v1/webhooks/'
    DELETE_WEBHOOK = '/v1/webhooks/{}'

    def post(self, payload):
        """
            Post webhook url to bamboohr for employee update or create
            Returns:
        """
        return self._post_request(self.POST_WEBHOOK, payload)

    def delete(self, id):
        """
            Delete Webhook
		    Returns:
        """
        return self._delete_request(self.DELETE_WEBHOOK.format(id))
