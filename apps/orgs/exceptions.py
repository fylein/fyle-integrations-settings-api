import logging
import traceback

from fyle.platform.exceptions import InternalServerError, InvalidTokenError, WrongParamsError


logger = logging.getLogger(__name__)
logger.level = logging.INFO


def handle_fyle_exceptions(task_name):
    def decorator(func):
        def new_fn(org_id: int, *args):
            error = {
                'task': task_name,
                'org_id': org_id,
                'alert': False,
                'message': None,
                'response': None
            }
            try:
                return func(org_id, *args)
            except InvalidTokenError:
                error['message'] = 'Invalid Fyle refresh token'

            except WrongParamsError as exception:
                error['message'] = exception.message
                error['response'] = exception.response
                error['alert'] = True

            except InternalServerError as exception:
                error['message'] = 'Internal server error while importing to Fyle'
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
