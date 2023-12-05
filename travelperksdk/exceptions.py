"""
TravelPerk SDK Exceptions
"""


class TravelperkSDKError(Exception):
    """The base exception class for Travelperk.

    Parameters:
        msg (str): Short description of the error.
        response: Error response from the API call.
    """

    def __init__(self, msg, response=None):
        super(TravelperkSDKError, self).__init__(msg)
        self.message = msg
        self.response = response

    def __str__(self):
        return repr(self.message)


class UnauthorizedClientError(TravelperkSDKError):
    """Wrong client secret and/or refresh token, 401 error."""


class ForbiddenClientError(TravelperkSDKError):
    """The user has insufficient privilege, 403 error."""


class BadRequestError(TravelperkSDKError):
    """Some of the parameters are wrong, 400 error."""


class NotFoundError(TravelperkSDKError):
    """Not found the item from URL, 404 error."""


class InternalServerError(TravelperkSDKError):
    """The rest TravelperkSDK errors, 500 error."""


class RateLimitError(TravelperkSDKError):
    """To many requests, 429 error."""
