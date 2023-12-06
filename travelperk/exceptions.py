"""
TravelPerk Exceptions
"""


class TravelperkError(Exception):
    """The base exception class for Travelperk.

    Parameters:
        msg (str): Short description of the error.
        response: Error response from the API call.
    """

    def __init__(self, msg, response=None):
        super(TravelperkError, self).__init__(msg)
        self.message = msg
        self.response = response

    def __str__(self):
        return repr(self.message)


class UnauthorizedClientError(TravelperkError):
    """Wrong client secret and/or refresh token, 401 error."""


class ForbiddenClientError(TravelperkError):
    """The user has insufficient privilege, 403 error."""


class BadRequestError(TravelperkError):
    """Some of the parameters are wrong, 400 error."""


class NotFoundError(TravelperkError):
    """Not found the item from URL, 404 error."""


class InternalServerError(TravelperkError):
    """The rest Travelperk errors, 500 error."""


class RateLimitError(TravelperkError):
    """To many requests, 429 error."""
