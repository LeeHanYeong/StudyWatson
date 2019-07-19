from .base import *

import_secrets()

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
# django-debug-toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]
