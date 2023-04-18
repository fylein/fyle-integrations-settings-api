import os

import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration

class Sentry:

    @staticmethod
    def init():
        sentry_sdk.init(
            dsn=os.environ.get('SENTRY_DSN'),
            send_default_pii=True,
            integrations=[DjangoIntegration()],
            environment=os.environ.get('SENTRY_ENV'),
            traces_sampler=Sentry.traces_sampler,
            attach_stacktrace=True,
            request_bodies='small',
            in_app_include=['apps.users',
            'apps.bamboohr',
            'apps.orgs',
            'apps.travelperk',
            'apps.gusto'
            'fyle_rest_auth'],
        )

    @staticmethod
    def traces_sampler(sampling_context):
        # avoiding ready APIs in performance tracing
        if sampling_context.get('wsgi_environ') is not None:
            if sampling_context['wsgi_environ']['PATH_INFO'] in ['/ready']:
                return 0

        return 0.5
    