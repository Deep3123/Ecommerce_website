"""
Django settings for e_shop project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-f9trs3#pg^&uyucvjp^jm(dlb+_2_)sd3w+jv*p)-l!lp+nw@2')
SECRET_KEY = 'django-insecure-f9trs3#pg^&uyucvjp^jm(dlb+_2_)sd3w+jv*p)-l!lp+nw@2'

# SECURITY WARNING: don't run with debug turned on in production!

# DEBUG = os.environ.get('DEBUG', 'True') == "True"
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'shop-genius.onrender.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'cart',
    'e_shop',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'e_shop.urls'

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
                'cart.context_processor.cart_total_amount',
            ],
        },
    },
]

WSGI_APPLICATION = 'e_shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'ecommerce_website',
#         'USER': 'root',
#         'PASSWORD': 'root',
#         'HOST': 'localhost',  # Or the IP address of your MySQL server
#         'PORT': '3306',        # Or the port your MySQL server is listening on
#     }
# }

# if not DEBUG:
#     DATABASES = {
#         "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
#     }
    
# else:
#     DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
    
    

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'kronosdp3123@gmail.com'
EMAIL_HOST_PASSWORD = 'lpkg oghn jwcq qhgz'

CART_SESSION_ID = 'cart'

RAZORPAY_KEY_ID = "rzp_test_pIqGo2X8aqQ6ja"
RAZORPAY_KEY_SECRET = "0YQOZh0MSElWcGefI3EiNU2b"

# settings.py

# Specify the languages your website supports.
# LANGUAGES = [
#     ('en', 'English'),
#     ('hi', 'Hindi'),
#     ('gu', 'Gujarati'),
#     ('ta', 'Tamil'),
# ]

# # Set the default language for your website.
# LANGUAGE_CODE = 'en'

# # Tell Django where to find the translation files.
# LOCALE_PATHS = [
#     os.path.join(BASE_DIR, 'locale'),
# ]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 1 week (in seconds)

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
