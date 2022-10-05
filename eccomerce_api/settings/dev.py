from .common import *


DEBUG = True

SECRET_KEY = 'django-insecure-6p%or!5c5_7e(#um8z)*!$tf93vt596p36#qfkwwa-=j)qrax('

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}