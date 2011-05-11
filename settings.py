import os

DEBUG = False

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Anton Ermak', 'anton@ermak.us'),
)

MANAGERS = ADMINS

DEFAULT_CHARSET='utf-8'

DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
EMAIL_HOST = 'localhost'
SERVER_EMAIL = 'robot@cloudpub.us'
SEND_BROKEN_LINK_EMAILS = True

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/Chicago'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
#LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1
SITE_DOMAIN = "cloudpub.us"
NODE_PORT = 9000

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'tnrm*t2b80nu51mgz3kc2%_v6bv8e)8rup$03m)dp7xb0)m8t9'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'openid_consumer.middleware.OpenIDMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'room.middleware.SiteMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "socialauth.context_processors.facebook_api_key",
    'django.core.context_processors.media',
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "userprofile.context_processors.css_classes"
)

ROOT_URLCONF = 'urls'

MEDIA_URL = '/site_media/'
MEDIA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'media')) + '/'

EDITOR_MEDIA_PATH = MEDIA_URL + 'editor/'
CATEGORIES_ALLOW_SLUG_CHANGE = True
CACHE_VIEW_LENGTH=10

SITE_NAME = 'cloudpub'

TEMPLATE_DIRS = (
     os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates')),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'mptt',
    'openid_consumer',
    'socialauth',
    'asterisk',
    'videostream',
    'editor',
    'categories',
    'userprofile',
    'room',
    'schedule',
)

LOGIN_URL = '/social/login'
LOGOUT_URL = '/socual/logout'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_ACTIVATION_DAYS = 7

PAGINATION=20

AWS_CALLING_FORMAT = 'REGULAR'

I18N_URLS = False
DEFAULT_AVATAR = os.path.join(MEDIA_ROOT, 'userprofile/generic.jpg')
AVATAR_WEBSEARCH = True
REQUIRE_EMAIL_CONFIRMATION = False
AVATAR_QUOTA = 8
AUTH_PROFILE_MODULE = "socialauth.profile"

OPENID_REDIRECT_NEXT = '/social/openid/done/'

OPENID_SREG = {"requred": "nickname, email, fullname",
               "optional":"postcode, country",
               "policy_url": ""}

OPENID_AX = [{"type_uri": "http://axschema.org/contact/email",
              "count": 1,
              "required": True,
              "alias": "email"},
             {"type_uri": "http://axschema.org/schema/fullname",
              "count":1 ,
              "required": False,
              "alias": "fname"}]

OPENID_AX_PROVIDER_MAP = {'Google': {'email': 'http://axschema.org/contact/email',
                                     'firstname': 'http://axschema.org/namePerson/first',
                                     'lastname': 'http://axschema.org/namePerson/last'},
                          'Default': {'email': 'http://axschema.org/contact/email',
                                      'fullname': 'http://axschema.org/namePerson',
                                      'nickname': 'http://axschema.org/namePerson/friendly'}
                          }

AUTHENTICATION_BACKENDS = (
    'socialauth.auth_backends.OpenIdBackend',
    'socialauth.auth_backends.TwitterBackend',
    'socialauth.auth_backends.FacebookBackend',
    'socialauth.auth_backends.LinkedInBackend',
    'django.contrib.auth.backends.ModelBackend',
)

try:
    from local import *
except ImportError:
    pass

