import logging
import traceback

from rest_framework.response import Response
from workato.exceptions import UnAuthorizedError, BadRequestError, NotFoundItemError, InternalServerError

logger = logging.getLogger(__name__)
logger.level = logging.INFO


def handle_workato_exception(task_name):
    def decorator(func):
        def new_fn(org_id: int, *args):
            error = {
                'task': task_name,
                'org_id': org_id,
                'message': None,
                'response': None
            }

            try:
                return func(org_id, *args)
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
