import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJ_DIR = os.path.dirname(BASE_DIR)

DEBUG = True

ALLOWED_HOSTS = ['staging.nnuh.org', ]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJ_DIR, 'public', 'media_staging')
STATIC_ROOT = os.path.join(PROJ_DIR, 'public', 'static')

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'nnuh_staging',
        'PASSWORD': 'pt5eeIfJ',
        'PORT': '',
        'USER': 'nnuh'
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'nnuh_staging' 
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch5_backend.Elasticsearch5SearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'nnuh_staging',
    },
    'en': {
        'ENGINE': 'haystack.backends.elasticsearch5_backend.Elasticsearch5SearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'nnuh_staging_en',
    },
    'ar': {
        'ENGINE': 'haystack.backends.elasticsearch5_backend.Elasticsearch5SearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'nnuh_staging_ar',
    },
}

DJANGOCMS_BOOTSTRAP4_CAROUSEL_ASPECT_RATIOS = (
    (2500, 925),
)

FILER_ENABLE_PERMISSIONS = False
FILER_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS = True
