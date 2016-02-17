"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
# -*- coding: utf-8 -*-

import os

# TODO gettext

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=mthwukkexh4p3qshr%ht_&g#r^=2x@=%#k429eu-&jqu3+(v3'

# SESSIONS
# TODO cookie stuff

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'True'

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

    'ids_auth',
    'ids_projects',
    'ids_specimens',
    'ids_datasets',
    'ids_data',
    'ids_systems',
]

AUTHENTICATION_BACKENDS = (
    'ids_auth.backends.AgaveOAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# TODO CACHES = {
# }

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
            ],
        },
    },
]

WSGI_APPLICATION = 'ids.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# TODO mysql if DATABASE_HOST (see designsafe)

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

# TODO STATIC_ROOT = ''

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'ids', 'static'),
)

# TODO STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# TODO STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#     'pipeline.finders.PipelineFinder',
# )

# TODO MEDIA_ROOT = ''

# TODO maybe djangocms

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# TODO maybe djangocms_forms

#####
#
# Bootstrap3 Settings
#
#####
BOOTSTRAP3 = {
    'required_css_class': 'required',
}

# TODO Django Impersonate

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

# TODO smtp

# TODO pipeline

# TODO agave

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