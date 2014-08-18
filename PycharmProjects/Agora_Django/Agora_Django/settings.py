"""
Django settings for Agora_Django project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p1($+45!k)pbtuuw4jc&2%)wf!c2#d11!(4)u2&phv(ba%@7xy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost',]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Agora',
    'Agora_git',
    'Agora_android',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
#'django.middleware.csrf.CsrfViewMiddleware',

ROOT_URLCONF = 'Agora_Django.urls'

WSGI_APPLICATION = 'Agora_Django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#Email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = "587"
EMAIL_HOST_USER = 'agoranotes@gmail.com'
EMAIL_HOST_PASSWORD = 'ng76ax1990'
EMAIL_USE_TLS = True

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    )

REPO_URL = 'repo/'
REPO_ROOT = os.path.join(BASE_DIR,  "repo")


TEMPLATE_DIRS = os.path.join(BASE_DIR,  'templates')

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = 'media/'


FILE_UPLOAD_MAX_MEMORY_SIZE = 3
# Directory where files larger than the above size are stored
FILE_UPLOAD_TEMP_DIR = os.path.join(BASE_DIR, "media/temp")
# Operating permissions for uploaded files (default 0600)
FILE_UPLOAD_PERMISSIONS = 0600

import django.contrib.auth
django.contrib.auth.LOGIN_URL = '/'