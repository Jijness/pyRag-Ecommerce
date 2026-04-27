import os
from pathlib import Path
import pymysql
pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-customer-service-key-xxx'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'rest_framework',
    'customers',
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'customer_db',
        'USER': 'root',
        'PASSWORD': os.environ.get('DB_PASSWORD', '123456'),
        'HOST': os.environ.get('DB_HOST', 'mysql'),
        'PORT': '3306',
    }
}

_DB_URL = os.environ.get('DATABASE_URL', '')
if _DB_URL:
    import re
    _m = re.match(r'mysql\+pymysql://([^:]+):([^@]+)@([^:/]+):?(\d+)?/(\w+)', _DB_URL)
    if _m:
        DATABASES['default']['USER'] = _m.group(1)
        DATABASES['default']['PASSWORD'] = _m.group(2)
        DATABASES['default']['HOST'] = _m.group(3)
        DATABASES['default']['PORT'] = _m.group(4) or '3306'
        DATABASES['default']['NAME'] = _m.group(5)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
USE_TZ = True
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'UNAUTHENTICATED_USER': None,
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',)
}
