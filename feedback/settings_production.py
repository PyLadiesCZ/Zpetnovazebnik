from feedback.settings import *
import os
import django_heroku

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
DEBUG = False

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# Set up the app for Heroku
# see: https://devcenter.heroku.com/articles/django-app-configuration#settings-py-changes

django_heroku.settings(locals())
