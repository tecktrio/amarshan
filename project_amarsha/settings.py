"""
Django settings for project_amarsha project.
Developed by amalbenny
"""

import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '500/day',
        'user': '500/day'
    }
}
# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'API',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'project_amarsha.middleware.Authenticate_User_Middleware',
]


ROOT_URLCONF = 'project_amarsha.urls'

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

WSGI_APPLICATION = 'project_amarsha.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = DATABASES={
    'default':
        {
            'ENGINE':'django.db.backends.mysql',
            'NAME': 'amarshan',
            'USER': 'root',
            'PASSWORD': '1234',
         }
        }

PASSWORD_HASHERS = [
  'django.contrib.auth.hashers.PBKDF2PasswordHasher',
  'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]
# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# setting static files
STATIC_URL              = '/static/'
STATIC_ROOT             = os.path.join(BASE_DIR, 'static/')

# setting up default values
DEFAULT_AUTO_FIELD      = 'django.db.models.BigAutoField'
DEFAULT_FILE_STORAGE    =   'API.StorageBackend.MediaStorage'

# Aws configuration
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_QUERYSTRING_AUTH    = True
AWS_ACCESS_KEY_ID       = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY   = config('AWS_SECRET_ACCESS_KEY')
AWS_SES_REGION_NAME     = config('AWS_SES_REGION_NAME')
AWS_SES_REGION_ENDPOINT = config('AWS_SES_REGION_ENDPOINT')

# social media credentials
INSTAGRAM_BUSINESS_ACCOUNT_ID   = config('INSTAGRAM_BUSINESS_ACCOUNT_ID')
FACEBOOK_PAGE_ID                =  config('FACEBOOK_PAGE_ID')
ACCESS_TOKEN_FACEBOOK_PAGE      = config('ACCESS_TOKEN_FACEBOOK_PAGE')

# access key to access amarshan api
ACCESS_TOKEN_FOR_AMARSHAN_APP = config('ACCESS_TOKEN_FOR_AMARSHAN_APP')

# setting up django email backend
EMAIL_BACKEND   = 'django_ses.SESBackend'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')#sender's email-id
