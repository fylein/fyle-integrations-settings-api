"""
Travelperk Webhooks
"""
from .api_base import ApiBase


class WebhooksSubscriptions(ApiBase):
    """Class for Webhooks Subscriptions APIs."""

    GET_WEBHOOK_SUBSCRIPTIONS = '/webhooks'
    POST_WEBHOOK_SUBSCRIPTIONS = '/webhooks'
    GET_WEBHOOK_SUBSCRIPTIONS_BY_ID = '/webhooks/{}'
    DELETE_WEBHOOK_SUBSCRIPTIONS = '/webhooks/{}'
    TEST_WEBHOOK_SUBSCRIPTIONS = '/webhooks/{}/test'

    def get_all(self):
        """Get a list of the existing Webhooks Subscriptions in the Organization.

        Returns:
            List with dicts in Webhooks Subscriptions schema.
        """
        return self._get_request('webhooks', WebhooksSubscriptions.GET_WEBHOOK_SUBSCRIPTIONS)

    def get_by_id(self, subscription_id):
        """Get a Webhooks Subscription in the Organization.

        Args:
            subscription_id (str): The id of the Webhooks Subscription.

        Returns:
            Dict in Webhooks Subscriptions schema.
        """
        return self._get_request('webhooks', WebhooksSubscriptions.GET_WEBHOOK_SUBSCRIPTIONS_BY_ID.format(subscription_id))

    def create(self, data):
        """Create a new Webhooks Subscription in the Organization.

        Args:
            data (dict): Dict in Webhooks Subscriptions schema.

        Returns:
            Dict in Webhooks Subscriptions schema.
        """
        return self._post_request(WebhooksSubscriptions.POST_WEBHOOK_SUBSCRIPTIONS, data=data)

    def delete(self, subscription_id):
        """Delete a Webhooks Subscription in the Organization.

        Args:
            subscription_id (str): The id of the Webhooks Subscription.

        Returns:
            Dict in Webhooks Subscriptions schema.
        """
        return self._delete_request(WebhooksSubscriptions.DELETE_WEBHOOK_SUBSCRIPTIONS.format(subscription_id))

    def test(self, subscription_id):
        """Test a Webhooks Subscription in the Organization.

        Args:
            subscription_id (str): The id of the Webhooks Subscription.

        Returns:
            Dict in Webhooks Subscriptions schema.
        """
        return self._post_request(WebhooksSubscriptions.TEST_WEBHOOK_SUBSCRIPTIONS.format(subscription_id))
