# Django settings for socialauthdemo project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

#DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#DATABASE_NAME = '/home/anton/yotaplay/data.db'              # Or path to database file if using sqlite3.
DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'yotaplay'              # Or path to database file if using sqlite3.
DATABASE_USER = 'root'             # Not used with sqlite3.
DATABASE_PASSWORD = 'daodeczin'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


DEFAULT_CHARSET='utf-8'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

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
    'video.middleware.VideoMiddleware',
    #'socialauth.middleware.FacebookConnectMiddleware'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "socialauth.context_processors.facebook_api_key",
    'django.core.context_processors.media',
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "video.context_processors.categories",
    "userprofile.context_processors.css_classes"
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.comments',
    'categories',
    'socialauth',
    'openid_consumer',
    'registration',
    'mptt',
    'categories',
    'editor',
    'voting',
    'tagging',
    'userprofile',
    'video',
    'django.contrib.admin',
)

LOGIN_URL = '/social/login'
LOGOUT_URL = '/socual/logout'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_ACTIVATION_DAYS = 7

PAGINATION=20

try:
    from localsettings import *
except ImportError:
    pass

import os
MEDIA_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media'))
MEDIA_URL = '/site_media/'
EDITOR_MEDIA_PATH = MEDIA_URL + 'editor/'
CATEGORIES_ALLOW_SLUG_CHANGE = True
CATEGORIES_RELATION_MODELS = ['video.movie']
CACHE_VIEW_LENGTH=10

SITE_NAME = 'cloudpub'

AWS_CALLING_FORMAT = 'REGULAR'

# START of django-profile specific options
I18N_URLS = False
DEFAULT_AVATAR = os.path.join(MEDIA_ROOT, 'userprofile/generic.jpg')
AVATAR_WEBSEARCH = True
# 127.0.0.1:8000 Google Maps API Key
REQUIRE_EMAIL_CONFIRMATION = False
AVATAR_QUOTA = 8
AUTH_PROFILE_MODULE = "socialauth.profile"

OPENID_REDIRECT_NEXT = '/social/openid/done/'

OPENID_SREG = {"requred": "nickname, email, fullname",
               "optional":"postcode, country",
               "policy_url": ""}

#example should be something more like the real thing, i think
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



## if any of this information is desired for your app
FACEBOOK_EXTENDED_PERMISSIONS = (
    #'publish_stream',
    #'create_event',
    #'rsvp_event',
    #'sms',
    #'offline_access',
    'email',
    #'read_stream',
    #'user_about_me',
    #'user_activites',
    #'user_birthday',
    #'user_education_history',
    #'user_events',
    #'user_groups',
    #'user_hometown',
    #'user_interests',
    #'user_likes',
    #'user_location',
    #'user_notes',
    #'user_online_presence',
    #'user_photo_video_tags',
    #'user_photos',
    #'user_relationships',
    #'user_religion_politics',
    #'user_status',
    #'user_videos',
    #'user_website',
    #'user_work_history',
    #'read_friendlists',
    #'read_requests',
    #'friend_about_me',
    #'friend_activites',
    #'friend_birthday',
    #'friend_education_history',
    #'friend_events',
    #'friend_groups',
    #'friend_hometown',
    #'friend_interests',
    #'friend_likes',
    #'friend_location',
    #'friend_notes',
    #'friend_online_presence',
    #'friend_photo_video_tags',
    #'friend_photos',
    #'friend_relationships',
    #'friend_religion_politics',
    #'friend_status',
    #'friend_videos',
    #'friend_website',
    #'friend_work_history',
)


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'socialauth.auth_backends.OpenIdBackend',
    'socialauth.auth_backends.TwitterBackend',
    'socialauth.auth_backends.FacebookBackend',
    'socialauth.auth_backends.LinkedInBackend',
)
