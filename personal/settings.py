"""
Django settings for personal project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "personal.settings")
# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
#
# from django.core.wsgi import get_wsgi_application
#
# application = get_wsgi_application()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', '0').lower() in ['true', 't', '1']

ALLOWED_HOSTS = ['timeenjoyed.dev', 'www.timeenjoyed.dev', '164.90.147.83', 'localhost']

# Application definition

INSTALLED_APPS = [

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Debug tool from "boxed" on Django server
    # 'django_fastdev',

    # WYSIWYG editor
    'ckeditor',

    # Sanitizer
    'django_bleach',

    # Import-Export JSON into Admin,
    'import_export',

    #Bootstrap calendar date picker
    # 'bootstrap5',
    # 'bootstrap_datepicker_plus',

    'django.contrib.sites',
    'allauth.account',
    'allauth.socialaccount',

    'allauth.socialaccount.providers.twitch',

    # twitch-auth login app
    'users',
    'login',

    # My apps
    'home',
    'blog',
]

# CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar': 'full',
        'extraPlugins': 'codesnippet',
    }
}

SITE_ID = 1

# Twitch-Auth

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ROOT_URLCONF = 'personal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # These templates override pre-defined templates:
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

# Turn off in development mode:
if not DEBUG:
    WSGI_APPLICATION = 'personal.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


if not DEBUG:

    # Reverse proxy related to nginx (from ChatGPT)

    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# DOCKER DATABASE SETTINGS:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'djangodb',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'db',
#         'PORT': '5432',
#     }
# }


# ACTUAL LOCAL DATABASE SETTINGS.

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': os.getenv('DATABASE_NAME'),

        'USER': os.getenv('DATABASE_USER'),

        'PASSWORD': os.getenv('DATABASE_PASS'),

        'HOST': os.getenv('HOST'),

        'PORT': os.getenv('PORT'),

    }
}

if DEBUG:
    LOGGING = {

        'version': 1,
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                # 'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
            },


        },
        'loggers': {
            'django.db.backends': {
                'level': 'DEBUG',
                'handlers': ['console'],
            },


        }
    }

if not DEBUG:

    LOGGING = {

            'version': 1,
            'filters': {
                'require_debug_true': {
                    '()': 'django.utils.log.RequireDebugTrue',
                }
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    # 'filters': ['require_debug_true'],
                    'class': 'logging.StreamHandler',
                },



                'file': {
                    'level': 'ERROR',
                    'class': 'logging.FileHandler',
                    'filename': '/var/log/gunicorn/error.log',
                }
            },
            'loggers': {
                'django.db.backends': {
                    'level': 'DEBUG',
                    'handlers': ['console'],
                },
                'django': {
                    'handlers': ['file'],
                    'level': 'ERROR',
                    'propagate': True,

                }
            }
        }



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'


STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Static files get taken from staticfiles_dir, and collected in STATIC_ROOT
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Override's django's default logout
LOGIN_REDIRECT_URL = "/profile/"
#
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'

# Twitch Auth Scopes

SOCIALACCOUNT_PROVIDERS = {
    'twitch': {
        'SCOPE': [''],
    }
}
