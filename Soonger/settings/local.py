import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'soonger',
        'USER': 'crab',
        'PASSWORD': 'Carlosrab*',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

MEDIA_URL = "http://localhost:8000/media/"
STATIC_URL = "http://localhost:8000/static/"
# ADMIN_MEDIA_PREFIX = "http://localhost:8000/static/admin/"

# Static configuration.
MEDIA_ROOT = BASE_DIR.child('media')
STATIC_ROOT = ''

STATICFILES_DIRS = [BASE_DIR.child('static')]