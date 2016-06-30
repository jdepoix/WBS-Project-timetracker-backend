from base import *


DEBUG = True
ENVIRONMENT = 'test'

DATABASES['test_project'] = {
    'ENGINE': CONF.get('database').get('engine'),
    'NAME': 'project',
    'USER': CONF.get('database').get('user'),
    'PASSWORD': CONF.get('database').get('password'),
    'HOST': CONF.get('database').get('host'),
    'PORT': CONF.get('database').get('port'),
}
