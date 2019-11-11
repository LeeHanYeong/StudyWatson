from .base import *

AWS_SECRETS_MANAGER_SECRETS_SECTION = 'study-watson:dev'
DEBUG = True
ALLOWED_HOSTS += SECRETS['ALLOWED_HOSTS']

INSTALLED_APPS += [
    'debug_toolbar',
]
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'querycount.middleware.QueryCountMiddleware',
]

# DRF
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += (
    'rest_framework.authentication.SessionAuthentication',
)

# django-debug-toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

# django-querycount
QUERYCOUNT = {
    'DISPLAY_DUPLICATES': 2,
}
