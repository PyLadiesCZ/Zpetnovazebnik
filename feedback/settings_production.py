import os
import sys

import django_heroku

from feedback.settings import *


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
DEBUG = False

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']


# Set up the app for Heroku
# see: https://devcenter.heroku.com/articles/django-app-configuration#settings-py-changes

django_heroku.settings(locals())


# Log to "sys.stdout" rather than the default stderr, so that Heroku logs pick
# up error tracebacks

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                        'pathname=%(pathname)s lineno=%(lineno)s ' +
                        'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
