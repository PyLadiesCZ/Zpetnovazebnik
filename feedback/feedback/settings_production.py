from mysite.settings import *
import dj_database_url
import os
DATABASES['default'] = dj_database_url.config()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']
DEBUG = True
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
