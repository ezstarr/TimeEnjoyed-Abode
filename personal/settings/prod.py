from .base import *


DEBUG = False

# Append hosts, not redefine
ALLOWED_HOSTS += ['timeenjoyed.dev', 'www.timeenjoyed.dev', '164.90.147.83']

# I am assuming this is your prod DB? This should be brought in via envvar
# base.py covers this already, but transferring to here to not break things.
# Take note, this is redefining/overriding DATABASES
DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': 'timeenjoyeddiscordbot',

        'USER': 'timeenjoyed2',

        'PASSWORD': 'budgie',

        'HOST': '192.168.0.14',

        'PORT': '5432',
    }
}
