from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'buppli',
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
