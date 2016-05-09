"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
# -*- coding: utf-8 -*-

import os, read_conf

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'not_very_secret')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bootstrap3',
    'django_bootstrap_breadcrumbs',

    'ids_auth',
    'ids_projects',
]

AUTHENTICATION_BACKENDS = (
    'ids_auth.backends.AgaveOAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'ids_auth.middleware.AgaveTokenRefreshMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ids.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'ids', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'ids.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('en-us', 'English'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = '/opt/ids/static/'
STATIC_URL = '/static/'

MEDIA_ROOT = '/opt/ids/media/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'ids', 'static'),
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

#####
#
# Bootstrap3 Settings
#
#####
BOOTSTRAP3 = {
    'required_css_class': 'required',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters' : {
        'default': {
            'format': '[DJANGO] %(levelname)s %(asctime)s %(module)s %(name)s.%(funcName)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propogate': True,
        },
        'ids': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'ids_projects': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'ids_specimens': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'ids_datasets': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'ids_data': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'ids_systems': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

##
# Agave
#
# Tenant Configuration
AGAVE_TENANT_ID = os.environ.get('AGAVE_TENANT_ID', 'iplantc.org')
AGAVE_TENANT_BASEURL = os.environ.get('AGAVE_TENANT_BASEURL', 'https://agave.iplantc.org/')
#
# Client Configuration
AGAVE_CLIENT_KEY = os.environ.get('AGAVE_CLIENT_KEY')
AGAVE_CLIENT_SECRET = os.environ.get('AGAVE_CLIENT_SECRET')
AGAVE_SUPER_TOKEN = os.environ.get('AGAVE_SUPER_TOKEN')
#
# Other agave stuff
AGAVE_TOKEN_SESSION_ID = 'agave_token'

#######################
# Object Descriptions #
#######################

OBJ_DESCR = read_conf.read()
