"""
Django settings for wbs_timetracker project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import sys
import os
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_FILEPATH = PROJECT_DIR + '/conf.json'

CONF = json.load(open(CONF_FILEPATH))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a7c=br_wnq7($(!*()#dtm*nbzz@^kq1v7+#)ni(@rb3g2_p9%'

ALLOWED_HOSTS = ['*',]

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'crispy_forms',
]

INTERNAL_APPS = [
    #api
    'api',

    #data
    'data.wbs_user',
    'data.legacy.id_wbs',
    'data.legacy.project',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + INTERNAL_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wbs_timetracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

WBS_ID_DATABSE_NAME = 'id_wbs'

DATABASES = {
    'default': {
        'ENGINE': CONF.get('database').get('engine'),
        'NAME': WBS_ID_DATABSE_NAME,
        'USER': CONF.get('database').get('user'),
        'PASSWORD': CONF.get('database').get('password'),
        'HOST': CONF.get('database').get('host'),
        'PORT': CONF.get('database').get('port'),
    }
}

TEST_RUNNER = 'core.test_utils.unmanaged_model_test_runner.UnmanagedModelTestRunner'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DATETIME_FORMAT': '%Y-%m-%d',
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = '{}/static'.format(PROJECT_DIR)
