"""
Django settings for wbs_timetracker project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import os
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASSWORD_FILEPATH = PROJECT_DIR + '/passwords.json'

PASSWORDS = json.load(open(PASSWORD_FILEPATH))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a7c=br_wnq7($(!*()#dtm*nbzz@^kq1v7+#)ni(@rb3g2_p9%'

ALLOWED_HOSTS = []

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

]

INTERNAL_APPS = [

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

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

WBS_ID_DATABSE_NAME = 'id_wbs'

DATABASES = {
    'default': {
        'ENGINE': PASSWORDS.get('database').get('engine'),
        'NAME': WBS_ID_DATABSE_NAME,
        'USER': PASSWORDS.get('database').get('user'),
        'PASSWORD': PASSWORDS.get('database').get('password'),
        'HOST': PASSWORDS.get('database').get('host'),
        'PORT': PASSWORDS.get('database').get('port'),
    }
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
