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



KINOPOISK_CONSUMER_KEY = '690e4c001b9010fe3439f1easd6c767b04c907256'
KINOPOISK_CONSUMER_SECRET = 'dew2a043823a246a4d3e22668d815e3b'

TWITTER_CONSUMER_KEY = 'djT9ge47Z2MPaKZcb0gQ'
TWITTER_CONSUMER_SECRET = 'nWYzLLBuX4XOIa3fbH43nOhlHmfwZ1frctIgIGWUtI'

FACEBOOK_APP_ID = '159179810783818'
FACEBOOK_API_KEY = 'a5572cffdc7028eb2934ad709aad759e'
FACEBOOK_SECRET_KEY = '8ee059b36dc5055428c527dc1d075f23'

LINKEDIN_CONSUMER_KEY = '3DR4u4DPZfDr9VTXnULjIPMFN1eUfaPvXUzRJPvMFQpCkNCTIqPlbnt-S9RRJa2j'
LINKEDIN_CONSUMER_SECRET = 'g5KCM44SkDTBajvtDW9kN1kG5g4gf1PvrvSREp25qn0Ub39lv32Ocs3jBeAGRMFC'

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
    'socialauth.auth_backends.KinopoiskBackend',
    'socialauth.auth_backends.OpenIdBackend',
    'socialauth.auth_backends.TwitterBackend',
    'socialauth.auth_backends.FacebookBackend',
    'socialauth.auth_backends.LinkedInBackend',
)
