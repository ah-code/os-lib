"""
Django settings for openshift project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import imp
import urlparse

#suit
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
	'django.core.context_processors.request',
	'django.contrib.auth.context_processors.auth',
)

ON_OPENSHIFT = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
     ON_OPENSHIFT = True

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'ascq#%bii8(tld52#(^*ht@pzq%=nyb7fdv+@ok$u^iwb@2hwh'

default_keys = { 'SECRET_KEY': 'vm4rl5*ymb@2&d_(gc$gb-^twq9w(u69hi--%$5xrh!xk(t%hw' }
use_keys = default_keys
if ON_OPENSHIFT:
     imp.find_module('openshiftlibs')
     import openshiftlibs
     use_keys = openshiftlibs.openshift_secure(default_keys)

SECRET_KEY = use_keys['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
if ON_OPENSHIFT:
     DEBUG = True
else:
     DEBUG = True

TEMPLATE_DEBUG = DEBUG

if DEBUG:
     ALLOWED_HOSTS = ['*']
else:
     ALLOWED_HOSTS = ['*',]

# Application definitions
INSTALLED_APPS = (
	'bootstrap3',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mptt',
    'booklib',
    'easy_thumbnails',
#    'social_auth',
    'django.contrib.sites',
	'registration',
	'haystack',
	'whoosh',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

#search backend
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

#fixes the site_id error with not registered sites
SITE_ID=1

#django registration period
ACCOUNT_ACTIVATION_DAYS = 7



GOOGLE_OAUTH2_CLIENT_ID      = '324497128720-7uv1qmfevh1hfv7lab7qnaphu61unef7.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET  = '94Za9a6cbcvwtpnepOQkPjr5'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# If you want configure the REDISCLOUD
if 'REDISCLOUD_URL' in os.environ and 'REDISCLOUD_PORT' in os.environ and 'REDISCLOUD_PASSWORD' in os.environ:
    redis_server = os.environ['REDISCLOUD_URL']
    redis_port = os.environ['REDISCLOUD_PORT']
    redis_password = os.environ['REDISCLOUD_PASSWORD']
    CACHES = {
        'default' : {
            'BACKEND' : 'redis_cache.RedisCache',
            'LOCATION' : '%s:%d'%(redis_server,int(redis_port)),
            'OPTIONS' : {
                'DB':0,
                'PARSER_CLASS' : 'redis.connection.HiredisParser',
                'PASSWORD' : redis_password,
            }
        }
    }
    MIDDLEWARE_CLASSES = ('django.middleware.cache.UpdateCacheMiddleware',) + MIDDLEWARE_CLASSES + ('django.middleware.cache.FetchFromCacheMiddleware',)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'
TEMPLATE_DIRS = (
     os.path.join(BASE_DIR,'templates'),
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if 'OPENSHIFT_MYSQL_DB_URL' in os.environ:
    url = urlparse.urlparse(os.environ.get('OPENSHIFT_MYSQL_DB_URL'))
 
    DATABASES = {
		'default': {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME': os.environ['OPENSHIFT_APP_NAME'],
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port,
        }
}
else:
     DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'python',  # Or path to database file if using sqlite3.
            'USER': 'admintM4RKd7',                      # Not used with sqlite3.
            'PASSWORD': 'j2gR9-Fd1neW',                  # Not used with sqlite3.
            'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
        }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = "/static/"

if 'OPENSHIFT_REPO_DIR' in os.environ:
    STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'static')
else:
    STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))


# Media files (uploads)
MEDIA_URL = "/media/"    
if 'OPENSHIFT_DATA_DIR' in os.environ:
    #MEDIA_ROOT = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'media')
	MEDIA_ROOT = os.environ.get(‘OPENSHIFT_REPO_DIR’, ”)+’/wsgi/static/media’
else:
    MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))

####dummy email-backend, used for debugging at the moment
###if DEBUG:
#EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
#EMAIL_FILE_PATH = os.path.join(MEDIA_ROOT, 'mails') # change this to a proper location	


###gmail as a smtp server to send registratation mails	
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'python.onlinelib@gmail.com'
EMAIL_HOST_PASSWORD = 'onlinelib...'
	
	
	
	
#login-url
LOGIN_URL          = '/login-form/'
LOGIN_REDIRECT_URL = '/logged-in/'
LOGIN_ERROR_URL    = '/login-error/'