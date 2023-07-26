"""

Django settings for Hotel_Management project.
Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u+(wsc5)914$&4ts=z0^-6sku7*m1v%%%483dus$0bhjiq$b-('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
ACCOUNT_ADAPTER = "user.adapter.LoginAdapter"



# Application definition

INSTALLED_APPS = [
    'adminlte3',
    'adminlte3_theme',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'hotels',
    'rooms',
    'user',
    'booking',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    "crispy_forms",
    "crispy_bootstrap4", 
    'extra_views',
    'celery', 
    'django_crontab',
    'django_celery_results',  
    'django_celery_beat',
]   

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"

CRISPY_TEMPLATE_PACK = "bootstrap4"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Hotel_Management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Hotel_Management.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME':"hotel_sys",
                    'USER': "postgres",
                    'PASSWORD': "swan",
                    'HOST': "localhost",
                    'PORT': "5432",
                }
            }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = 'static/'
# MEDIA_ROOT= os.path.join(BASE_DIR, "media")
# MEDIA_URL="/media/"
STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = [STATIC_DIR]
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

AUTHENTICATION_BACKENDS =[    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
] 

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.HotelUser'


AUTHENTICATION_BACKENDS = [
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    
]


SITE_ID = 1

LOGIN_URL = 'admin_template/accounts/login/'

LOGIN_REDIRECT_URL = '/'

ACCOUNT_LOGOUT_REDIRECT_URL = '/'

ACCOUNT_SIGNUP_REDIRECT_URL = "/accounts/login/"

ACCOUNT_LOGOUT_ON_GET = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_FORMS = {
    'signup': 'user.custom_form.CustomSignupForm',

    
    "login": "allauth.account.forms.LoginForm",
    "add_email": "allauth.account.forms.AddEmailForm",
    "change_password": "allauth.account.forms.ChangePasswordForm",
    "set_password": "allauth.account.forms.SetPasswordForm",
    "reset_password": "allauth.account.forms.ResetPasswordForm",
    "reset_password_from_key": "allauth.account.forms.ResetPasswordKeyForm",
    "disconnect": "allauth.socialaccount.forms.DisconnectForm",
}


APP_LOG_FILENAME = os.path.join(BASE_DIR, "log/app.log")
ERROR_LOG_FILENAME = os.path.join(BASE_DIR, "log/error.log")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}
CELERY_RESULT_BACKEND = "django-db"
CELERY_TIMEZONE = "Asia/Kolkata"
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True
CELERY_TASK_TRACK_STARTED = True

CELERY_CACHE_BACKEND = 'default'

# django setting.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}