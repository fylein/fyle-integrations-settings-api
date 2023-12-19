import logging
import traceback

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


def handle_fyle_exceptions(task_name):
    def decorator(func):
        def new_fn(workspace_id: int, *args):
            error = {'task': task_name, 'workspace_id': workspace_id, 'alert': False, 'message': None, 'response': None}
            try:
                return func(workspace_id, *args)
            except InvalidTokenError:
                error['message'] = 'Invalid Fyle refresh token'

            except WrongParamsError as exception:
                error['message'] = exception.message
                error['response'] = exception.response
                error['alert'] = True

            except InternalServerError as exception:
                error['message'] = 'Internal server error'
                error['response'] = exception.__dict__

            except Exception:
                response = traceback.format_exc()
                error['message'] = 'Something went wrong'
                error['response'] = response
                error['alert'] = True

            if error['alert']:
                logger.error(error)
            else:
                logger.info(error)

        return new_fn

    return decorator
