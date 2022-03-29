from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_test',
        'USER': 'user_',
        'PASSWORD': 'secret_pw',
        'HOST': 'db',  # referencing docker db here
        'PORT': 3306,
        'MYSQL_ALLOW_EMPTY_PASSWORD': 'yes',
        'ATOMIC_REQUESTS': True
    }
}

if bool(GITHUB_WORKFLOW):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': '127.0.0.1',
            'PORT': 5432,
            'ATOMIC_REQUESTS': DEBUG
        }
    }
