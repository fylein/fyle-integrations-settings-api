import logging
import traceback

from django.http import JsonResponse

from workato.exceptions import UnAuthorizedError, BadRequestError, NotFoundItemError, InternalServerError

logger = logging.getLogger(__name__)
logger.level = logging.INFO


def handle_exception(task_name):
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
                logger.error(error)
                return JsonResponse(error, status=401)

            except NotFoundItemError as exception:
                error['message'] = exception.message
                error['response'] = exception.response
                logger.error(error)
                return JsonResponse(error, status=404)

            except BadRequestError as exception:
                error['message'] = exception.message
                error['response'] = exception.response
                logger.error(error)
                return JsonResponse(error, status=400)

            except InternalServerError as exception:
                error['message'] = exception.message
                error['response'] = exception.response
                logger.error(error)
                return JsonResponse(error, status=500)

            except Exception:
                response = traceback.format_exc()
                error['message'] = 'Something went wrong'
                error['response'] = response
                logger.error(error)
                return JsonResponse(error, status=500)

        return new_fn

    return decorator
