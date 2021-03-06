"""
Django settings for vuforia_cms project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, json
#BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# from "TDD with Python"
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z)_b!(^542#an9lfvx=thzz_)l4hbj_#mrbe=4g*fscps0arw4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['marker-staging.tengyan.space']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cms',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'vuforia_cms.urls'

WSGI_APPLICATION = 'vuforia_cms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

key_path = os.path.join(BASE_DIR, '../accesskey.json')
with open(key_path, "r", encoding="utf-8") as key_fp:
    key_dict = json.load(key_fp)
MYSQL_PW = key_dict['MYSQL_PW']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 「TDD with Python」p.141より (デプロイ時に)
        'NAME': os.path.join(BASE_DIR, '../database/db.sqlite3'),
    }

    # MySQLを使う場合。
    #'default': {
    #    # $ pip install mysql-connector-python --allow-external \
    #    # mysql-connector-python
    #    #'ENGINE': 'django.db.backends.mysql',
    #    'ENGINE': 'mysql.connector.django',
    #    'NAME': 'vuforia_cms',
    #    'USER': 'test',
    #    'PASSWORD': MYSQL_PW,
    #    'HOST': '',
    #}
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'ja'
# LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tokyo'
# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# 「TDD with Python」p.141より (デプロイ時に変更する)
STATIC_ROOT = os.path.join(BASE_DIR, '../static')

#MEDIA_ROOT = os.path.join(BASE_DIR, 'cms/media')
# 「TDD with Python」p.141より (デプロイ時に)
MEDIA_ROOT = os.path.join(BASE_DIR, '../media')
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'cms.UserProfile'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = 'login'

# SSL
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

DATE_INPUT_FORMATS = [
    '%Y-%m-%d','%m/%d/%Y', '%m/%d/%y', # '2006-10-25', '10/25/2006', '10/25/06'
    '%Y/%m/%d', # '2006/10/25'(デフォルトではない)
    '%b %d %Y', '%b %d, %Y', # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y', # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y', # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y', # '25 October 2006', '25 October, 2006'
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            },
        #'to_file': {
        #    'formatter': 'simple',
        #    'level': 'DEBUG',
        #    'class': 'logging.FileHandler',
        #    'filename': '/Users/js/Desktop/django.log',
        #},
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        #'django_site': {
        #    'handlers': ['to_file'],
        #    'level': 'DEBUG',
        #    'propagate': True,
        #},
    },
    'root': {'level': 'INFO'}
}
