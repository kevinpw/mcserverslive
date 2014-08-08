"""
Django settings for mcserverslive project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Application definition

INSTALLED_APPS = (

	'accounts',
	'mcserverslive',
	'mcstatus',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

	'registration',
	'captcha',
	'dajaxice',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mcserverslive.urls'

WSGI_APPLICATION = 'mcserverslive.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# import local_settings
from local_settings import *

# global template context
import django.conf.global_settings as DEFAULT_SETTINGS
TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
	"django.core.context_processors.request",
	"accounts.context_processors.include_login_form",
	"accounts.context_processors.domain",
)
TEMPLATE_LOADERS = DEFAULT_SETTINGS.TEMPLATE_LOADERS + (
	'django.template.loaders.eggs.Loader',
)
STATICFILES_FINDERS = DEFAULT_SETTINGS.STATICFILES_FINDERS + (
	'dajaxice.finders.DajaxiceFinder',
)

