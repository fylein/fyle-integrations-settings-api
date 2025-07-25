"""
Django settings for admin_settings project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
import sys

import dj_database_url

from .sentry import Sentry

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('DEBUG') == 'True' else False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',

    # Installed Apps
    'rest_framework',
    'fyle_rest_auth',
    'django_filters',
    'django_q',

    # User Created Apps
    'apps.users',
    'apps.bamboohr',
    'apps.orgs',
    'apps.travelperk',
    'apps.integrations',
    'apps.fyle_hrms_mappings',
    'apps.internal',
    'fyle_accounting_library.rabbitmq',
    'fyle_accounting_library.fyle_platform'
]

MIDDLEWARE = [
    'request_logging.middleware.LoggingMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'admin_settings.logging_middleware.ErrorHandlerMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'admin_settings.urls'
APPEND_SLASH = False

AUTH_USER_MODEL = 'users.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

FYLE_REST_AUTH_SETTINGS = {
    'async_update_user_settings_api': True    
}

FYLE_REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'apps.users.serializers.UserSerializer'
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'fyle_rest_auth.authentication.FyleJWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_THROTTLE_CLASSES': [
        'admin_settings.throttles.PerUserPathThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'per_user_path': '30/second'
    }
}

Q_CLUSTER = {
    'name': 'integrations_settings_api',
    'save_limit': 0,
    'retry': 14400,
    'timeout': 3600,
    'catch_up': False,
    'workers': 4,
    # How many tasks are kept in memory by a single cluster.
    # Helps balance the workload and the memory overhead of each individual cluster
    'queue_limit': 10,
    'cached': False,
    'orm': 'default',
    'ack_failures': True,
    'poll': 1,
    'max_attempts': 1,
    'attempt_count': 1,
    # The number of tasks a worker will process before recycling.
    # Useful to release memory resources on a regular basis.
    'recycle': 50,
    # The maximum resident set size in kilobytes before a worker will recycle and release resources.
    # Useful for limiting memory usage.
    'max_rss': 100000 # 100mb
}

SERVICE_NAME = os.environ.get('SERVICE_NAME')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '{levelname} %s {asctime} {module} {message} ' % SERVICE_NAME,
            'style': '{',
        },
        'requests': {
            'format': 'request {levelname} %s {asctime} {message}' % SERVICE_NAME,
            'style': '{'
        }
    },
    'handlers': {
        'debug_logs': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        },
        'request_logs': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'requests'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['request_logs'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['request_logs'],
            'propagate': False
        },
        'admin_settings': {
            'handlers': ['debug_logs'],
            'level': 'ERROR',
            'propagate': False
        },
        'apps': {
            'handlers': ['debug_logs'],
            'level': 'ERROR',
            'propagate': False
        },
        'gunicorn': {
            'handlers': ['request_logs'],
            'level': 'INFO',
            'propagate': False
        }
    }
}


WSGI_APPLICATION = 'admin_settings.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config()
}

DATABASES['default']['DISABLE_SERVER_SIDE_CURSORS'] = True

DATABASES['cache_db'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'cache.db'
}

DATABASE_ROUTERS = ['admin_settings.cache_router.CacheRouter']

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

API_URL = os.environ.get('API_URL')
FYLE_TOKEN_URI = os.environ.get('FYLE_TOKEN_URI')
FYLE_CLIENT_ID = os.environ.get('FYLE_CLIENT_ID')
FYLE_CLIENT_SECRET = os.environ.get('FYLE_CLIENT_SECRET')
FYLE_BASE_URL = os.environ.get('FYLE_BASE_URL')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SENDGRID_EMAIL = os.environ.get('SENDGRID_EMAIL')
BASE_URI = os.environ.get('BASE_URI')

GUSTO_CLIENT_ID = os.environ.get('GUSTO_CLIENT_ID')
GUSTO_CLIENT_SECRET = os.environ.get('GUSTO_CLIENT_SECRET')
GUSTO_ENVIRONMENT = os.environ.get('GUSTO_ENVIRONMENT')
TRAVELPERK_CLIENT_ID = os.environ.get('TRAVELPERK_CLIENT_ID')
TRAVELPERK_CLIENT_SECRET = os.environ.get('TRAVELPERK_CLIENT_SECRET')
TRAVELPERK_ENVIRONMENT = os.environ.get('TRAVELPERK_ENVIRONMENT')
TKWEBHOOKS_SECRET = os.environ.get('TKWEBHOOKS_SECRET')
TRAVELPERK_AUTH_URL = os.environ.get('TRAVELPERK_AUTH_URL')
TRAVELPERK_TOKEN_URL = os.environ.get('TRAVELPERK_TOKEN_URL')
TRAVELPERK_BASE_URL = os.environ.get('TRAVELPERK_BASE_URL')
TRAVELPERK_REDIRECT_URI = os.environ.get('TRAVELPERK_REDIRECT_URI')
FYLE_NOTIFICATIONS_EMAIL = os.environ.get('FYLE_NOTIFICATIONS_EMAIL')

CORS_ORIGIN_ALLOW_ALL = True

# Sentry
Sentry.init()

CORS_ALLOW_HEADERS = [
    'sentry-trace',
    'authorization',
    'content-type'
]

# Environ Variable Required for Tests
FYLE_REFRESH_TOKEN = os.environ.get('FYLE_REFRESH_TOKEN')
