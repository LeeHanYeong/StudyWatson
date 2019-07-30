from .base import *

import_secrets()

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# DRF
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += (
    'rest_framework.authentication.SessionAuthentication',
)

# django-debug-toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]
