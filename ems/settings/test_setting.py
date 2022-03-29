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


REST_FRAMEWORK['TEST_REQUEST_DEFAULT_FORMAT'] = 'json'
