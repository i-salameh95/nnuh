import os  # isort:skip
gettext = lambda s: s
DATA_DIR = os.path.dirname(os.path.dirname(__file__))
"""
Django settings for conf project.

Generated by 'django-admin startproject' using Django 2.1.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJ_DIR = os.path.dirname(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&pz@gtby!65=j(&kvf74xi^355u1xu=d*_k#dud^dxzi4^k2lw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['dev.nnuh.org','www.nnuh.org','nnuh.org','212.14.237.226']


# Application definition



ROOT_URLCONF = 'conf.urls'



WSGI_APPLICATION = 'conf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases




# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Asia/Gaza'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJ_DIR, 'public', 'media')
STATIC_ROOT = os.path.join(PROJ_DIR, 'public', 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'conf', 'static'),
)
SITE_ID = 1


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'conf', 'templates'),],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.template.context_processors.static',
                'cms.context_processors.cms_settings',
                'nnuh_search.context_processors.search_form',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ],
        },
    },
]


MIDDLEWARE = [
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'nnuh_doctors.middleware.ForceResponseMiddleware',
    'nnuh_contact.middleware.ForceResponseMiddleware',
]

INSTALLED_APPS = [
    'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'filer',
    'easy_thumbnails',
    'djangocms_column',
    'djangocms_file',
    'djangocms_style',
    'djangocms_snippet',
    'djangocms_googlemap',
    'djangocms_video',
    
    'djangocms_icon',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_bootstrap4',
    'djangocms_bootstrap4.contrib.bootstrap4_alerts',
    'djangocms_bootstrap4.contrib.bootstrap4_badge',
    'djangocms_bootstrap4.contrib.bootstrap4_card',
    'djangocms_bootstrap4.contrib.bootstrap4_carousel',
    'djangocms_bootstrap4.contrib.bootstrap4_collapse',
    'djangocms_bootstrap4.contrib.bootstrap4_content',
    'djangocms_bootstrap4.contrib.bootstrap4_grid',
    'djangocms_bootstrap4.contrib.bootstrap4_jumbotron',
    'djangocms_bootstrap4.contrib.bootstrap4_link',
    'djangocms_bootstrap4.contrib.bootstrap4_listgroup',
    'djangocms_bootstrap4.contrib.bootstrap4_media',
    'djangocms_bootstrap4.contrib.bootstrap4_picture',
    'djangocms_bootstrap4.contrib.bootstrap4_tabs',
    'djangocms_bootstrap4.contrib.bootstrap4_utilities',

    'absolute',
    'aldryn_forms',
    'aldryn_forms.contrib.email_notifications',
    'captcha',
    'emailit',
    # 'filer',

    'aldryn_apphooks_config',
    'aldryn_categories',
    'aldryn_common',
    'aldryn_newsblog',
    'aldryn_people',
    'aldryn_translation_tools',
    'parler',
    'sortedm2m',
    'taggit',
    'bootstrap_pagination',

    'django_select2',
    'haystack',
    'aldryn_search',
    'standard_form',
    'spurl',
    'webpack_loader',
    'crispy_forms',
    'fullurl',
    'conf',
    'nnuh_search',
    'nnuh_contact',
    'nnuh_doctors',
    'djangocms_htmlsitemap',
]

LANGUAGES = (
    ## Customize this
    ('en', gettext('en')),
    ('ar', gettext('ar')),
)

CMS_LANGUAGES = {
    ## Customize this
    1: [
        {
            'code': 'en',
            'name': gettext('en'),
            'redirect_on_fallback': True,
            'public': True,
            'hide_untranslated': True,
        },
        {
            'code': 'ar',
            'name': gettext('ar'),
            'redirect_on_fallback': True,
            'public': True,
            'hide_untranslated': True,
        },
    ],
    'default': {
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': True,
    },
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch5_backend.Elasticsearch5SearchEngine',
        'URL': 'http://search:9200/',
        'INDEX_NAME': 'nnuh_default',
    },
    'en': {
        'ENGINE': 'haystack.backends.elasticsearch5_backend.Elasticsearch5SearchEngine',
        'URL': 'http://search:9200/',
        'INDEX_NAME': 'nnuh_en',
    },
    'ar': {
        'ENGINE': 'haystack.backends.elasticsearch5_backend.Elasticsearch5SearchEngine',
        'URL': 'http://search:9200/',
        'INDEX_NAME': 'nnuh_ar',
    },
}

HAYSTACK_ROUTERS = ['aldryn_search.router.LanguageRouter',]


CMS_TEMPLATES = (
    ## Customize this
    ('fullwidth.html', 'Fullwidth'),
    ('sidebar_left.html', 'Sidebar Left'),
    ('sidebar_right.html', 'Sidebar Right'),
    ('homepage.html', 'Homepage'),
)

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'db',
        'NAME': 'nnuh',
        'PASSWORD': 'secret',
        'PORT': '',
        'USER': 'root'
    }
}

MIGRATION_MODULES = {

}


from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}


CRISPY_TEMPLATE_PACK = 'bootstrap4'


THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

DJANGOCMS_LINK_USE_SELECT2 = True

from django.utils.translation import ugettext_lazy as _

DJANGOCMS_BOOTSTRAP4_COLOR_STYLE_CHOICES = (
    ('primary', _('Primary - Terequaz')),
    ('secondary', _('Secondary - Light Terequaz')),
    ('violet', _('Violet')),
    ('success', _('Success')),
    ('danger', _('Danger')),
    ('warning', _('Warning')),
    ('info', _('Info')),
    ('light', _('Light')),
    ('dark', _('Dark')),
)

DJANGOCMS_BOOTSTRAP4_CAROUSEL_TEMPLATES = (
    ('default', _('Default')),
    ('featured', _('Featured')),
)

DJANGOCMS_BOOTSTRAP4_CAROUSEL_ASPECT_RATIOS = (
    (2500, 925),
)

DJANGOCMS_ICON_TEMPLATES = [
    ('media', 'Media Icon'),
    ('accordion', 'Accordion Icon'),
    ('featured', 'Featured'),
]

DJANGOCMS_STYLE_CHOICES = ['container', 'content', 'teaser', 'copyrights']

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': '', # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'conf', 'static', 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map']
    }
}

DJANGOCMS_FILE_TEMPLATES = [
    ('featured', 'Featured'),
]