"""
Django settings for admin_settings project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
import sys

import dj_database_url

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

    # User Created Apps
    'apps.users',
    'apps.bamboohr',
    'apps.orgs'
]

MIDDLEWARE = [
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
        }
    }
}


WSGI_APPLICATION = 'admin_settings.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
if os.environ.get('DATABASE_URL', ''):
    DATABASES = {
        'default': dj_database_url.config()
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'OPTIONS': {
                'options': '-c search_path={0}'.format(os.environ.get('DB_SCHEMA'))
            },
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT'),
        }
    }

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
FYLE_APP_URL = os.environ.get('APP_URL')

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = [
    'sentry-trace',
    'authorization',
    'content-type'
]
