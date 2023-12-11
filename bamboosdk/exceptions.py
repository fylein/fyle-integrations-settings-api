"""
BambooHR SDK exceptions
"""


class BambooHrSDKError(Exception):
    """
    The base exception class for BambooHR SDK
    """

    def __init__(self, msg, response=None):
        super(BambooHrSDKError, self).__init__(msg)
        self.message = msg
        self.response = response

    def __str__(self):
        return repr(self.message)


class NoPrivilegeError(BambooHrSDKError):
    """The user has insufficient privilege, 403 error."""

class NotFoundItemError(BambooHrSDKError):
    """Not found the item from URL, 404 error."""

class InvalidTokenError(BambooHrSDKError):
    """Invalid or non-existing access token, 401 error"""
