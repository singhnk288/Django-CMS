"""
Django settings for djfirst project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gbiwhokjmf9-8vgj$^8uxz!f+5crx(7uy+u%6*0+36nh3r+k$8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # added Account App - Neeraj Kumar
    'account',
    # added cms master App - Neeraj Kumar
    'cms_master',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'auditlog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
        # Write Custom Middleware
    'djfirst.middleware.WebInitialization',
    'auditlog.middleware.AuditlogMiddleware',
]

ROOT_URLCONF = 'djfirst.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djfirst.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'django-cms',
        'HOST': 'mongodb://neeraj:neeraj@127.0.0.1:27017/?authSource=admin',
        'USER': 'neeraj',
        'PASSWORD': 'neeraj',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
# you can put static files which apply to your entire project here
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    '/Django/djfirst/djfirst/static',
]

# Multi-Language Site Support :
# We need to translate language from laguage file
# Provide a lists of languages which your site supports.
LANGUAGES = (
    ('en', _('English')),
    #('hi', _('Hindi')),    
)

#Global Variable Define
APP_NAME = 'Recall Info'

# APP URL
APP_URL = 'http://127.0.0.1:8000/'
# Set Default Lanugage Id and code
DEFAULT_LANGUAGE_ID = 1
# Set the default language for your site.
LANGUAGE_CODE = 'en'
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Remove unwanted Warining
SILENCED_SYSTEM_CHECKS = ['urls.W002', 'security.W019']

# Login Url : Define in Settings.py file
LOGIN_URL = '/accounts/login/'

# Home Page Url Set
HOME_URL = '/master/language'
