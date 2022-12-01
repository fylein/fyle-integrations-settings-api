"""
    Contains Workato Exceptions
"""

class WorkatoError(Exception):
    """The base exception class for workato module
    
    Parameters:
        msg (str): Short description of the error.
        response: Error response from API call
    """
    
    def __init__(self, msg, response=None):
        super().__init__(msg)
        self.message = msg
        self.response = response
        
    def __str__(self):
        return repr(self.message)
        

class UnAuthorizedError(WorkatoError):
    """Workato Authentication Failed, 401 error"""

    
class BadRequestError(WorkatoError):
    """Workato validation Exception Error, 400 error"""
    

class NotFoundItemError(WorkatoError):
     """Not found the item from URL, 404 error."""


class InternalServerError(WorkatoError):
    """Internal server error, 500 error"""
