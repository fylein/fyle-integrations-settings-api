import logging
import traceback

from rest_framework.views import status
from rest_framework.response import Response
from fyle.platform.exceptions import InternalServerError, InvalidTokenError, WrongParamsError
from workato.exceptions import UnAuthorizedError, BadRequestError, NotFoundItemError, InternalServerError

logger = logging.getLogger(__name__)
logger.level = logging.INFO


def handle_workato_exception(task_name):
    def decorator(func):
        def new_fn(org_id: int, *args, **kwargs):
            error = {
                'task': task_name,
                'org_id': org_id,
                'message': None,
                'response': None
            }

            try:
                return func(org_id, *args, **kwargs)
            except UnAuthorizedError as exception:
                error['message'] = exception.message
                error['response'] = exception.response
                logger.info(error)
                return Response(error, status=401)

            except NotFoundItemError as exception:
                error['message'] = exception.message
                error['response'] = exception.response
                logger.error(error)
                return Response(error, status=404)

            except BadRequestError as exception:
                error['message'] = exception.message
                error['response'] = exception.response
                logger.error(error)
                return Response(error, status=400)

            except InternalServerError as exception:
                error['message'] = exception.message
                error['response'] = exception.response
                logger.error(error)
                return Response(error, status=500)

            except Exception:
                response = traceback.format_exc()
                error['message'] = 'Something went wrong'
                error['response'] = response
                logger.error(error)
                return Response(error, status=500)

        return new_fn

    return decorator


def handle_fyle_exceptions():
    def decorator(func):
        def new_fn(*args, **kwargs):
            error = {'org_id': kwargs['org_id'], 'alert': False, 'message': None, 'response': None}
            try:
                return func(*args, **kwargs)

            except InvalidTokenError:
                error['message'] = 'Invalid Fyle refresh token'
                return Response(data={'message': error}, status=status.HTTP_400_BAD_REQUEST)

            except WrongParamsError as exception:
                error['message'] = exception.message
                error['response'] = exception.response
                error['alert'] = True
                logger.error(error)
                return Response(data={'message': error}, status=status.HTTP_400_BAD_REQUEST)

            except InternalServerError as exception:
                error['message'] = 'Internal server error'
                error['response'] = exception.__dict__
                return Response(data={'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception:
                response = traceback.format_exc()
                error['message'] = 'Something went wrong'
                error['response'] = response
                error['alert'] = True
                logger.error(error)
                return Response(data={'message': 'An unhandled error has occurred, please re-try later'}, status=status.HTTP_400_BAD_REQUEST)

        return new_fn

    return decorator
