import os

import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration
import gevent

class Sentry:

    @staticmethod
    def init():
        sentry_sdk.init(
            dsn=os.environ.get('SENTRY_DSN'),
            send_default_pii=True,
            integrations=[DjangoIntegration()],
            environment=os.environ.get('SENTRY_ENV'),
            attach_stacktrace=True,
            before_send=Sentry.before_send,
            max_request_body_size='small',
            in_app_include=[
                'apps.users',
                'apps.bamboohr',
                'apps.orgs',
                'apps.travelperk',
                'fyle_rest_auth'
            ],
        )

    @staticmethod
    def before_send(event, hint):
        if 'exc_info' in hint:
            exc_type, exc_value, tb = hint['exc_info'] 
            if isinstance(exc_value, (gevent.GreenletExit)):
                return None
            elif exc_value.args[0] in ['Error: 502']:
                return None
        return event
    