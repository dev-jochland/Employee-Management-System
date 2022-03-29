import os
from datetime import timedelta
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env_file = Path.joinpath(BASE_DIR, '../.env').as_posix()
environ.Env.read_env(env_file)

SECRET_KEY = 'test_secret_key'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    # Default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # User created apps
    'user.apps.UserConfig',

    # Third party apps
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ems.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'ems.wsgi.application'

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

LANGUAGE_CODE = 'en-uk'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configure simple-jwt
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=3600),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'email',
    'USER_ID_CLAIM': 'user_email',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=15),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
}

# Configure dj-rest-auth
REST_USE_JWT = True
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = True

# Configure django-allauth
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'

SITE_ID = 1

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'user.serializers.user_serializer.JWTUserDetailSerializer',
    'LOGIN_SERIALIZER': 'user.serializers.login_serializer.CustomLoginSerializer',
    'JWT_TOKEN_CLAIMS_SERIALIZER': 'user.serializers.user_serializer.CustomTokenObtainPairSerializer',
}

# Custom Serializer to handle organisation signup
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'user.serializers.register_serializer.CustomRegisterSerializer',
}

ACCOUNT_ADAPTER = 'user.adapters.CustomUserAccountAdapter'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTTokenUserAuthentication',
    ],
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

AUTH_USER_MODEL = 'user.AppUser'

# Celery Configuration Options
CELERY_TIMEZONE = "Africa/Lagos"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['json', 'pickle']
CELERY_TASK_SERIALIZER = 'pickle'  # could be json too, changed it to pickle because I added apply_async
CELERY_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 1
CELERYD_TASK_SOFT_TIME_LIMIT = 60  # secs
# CELERY_ROUTES = {
#  'user.tasks.*': {'queue': 'make_bulk_payment'},
# }

DJANGO_ADMIN_PASSWORD = 'testpassword'

DJANGO_ADMIN_EMAIL = 'testuser@testuser.com'

GITHUB_WORKFLOW = 1
