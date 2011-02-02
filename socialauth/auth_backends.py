from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
import facebook

import urllib
from socialauth.lib import oauthtwitter2 as oauthtwitter
from socialauth.models import Profile
from socialauth.lib.linkedin import *

import random


TWITTER_CONSUMER_KEY = getattr(settings, 'TWITTER_CONSUMER_KEY', '')
TWITTER_CONSUMER_SECRET = getattr(settings, 'TWITTER_CONSUMER_SECRET', '')

FACEBOOK_APP_ID = getattr(settings, 'FACEBOOK_APP_ID', '')
FACEBOOK_API_KEY = getattr(settings, 'FACEBOOK_API_KEY', '')
FACEBOOK_SECRET_KEY = getattr(settings, 'FACEBOOK_SECRET_KEY', '')

LINKEDIN_CONSUMER_KEY = getattr(settings, 'LINKEDIN_CONSUMER_KEY', '')
LINKEDIN_CONSUMER_SECRET = getattr(settings, 'LINKEDIN_CONSUMER_SECRET', '')

OPENID_AX_PROVIDER_MAP = getattr(settings, 'OPENID_AX_PROVIDER_MAP', {})


def random_username():
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for i in xrange(10)])


class ProfileData(object):
    pass

def update_profile(user,provider,uid,data):

    def def_val(name, val):
        if not hasattr(data,name) or getattr(data,name) is None:
             setattr(data,name,val)
    profile = None

    try:
        profile = Profile.objects.get(uid = uid)
    except Profile.DoesNotExist:
	profile = Profile()
        pass
 
    if not user or not user.is_authenticated():
        user = User()
    else:
        user = User.objects.get( username=user.username )
                
    def_val('username', random_username())
    def_val('email', data.username + "@mail.cloudpub.us" )
    def_val('first_name', "-")
    def_val('last_name', "-")

    data.provider = provider

    for k,v in data.__dict__.iteritems():
        setattr(user, k, v)
        setattr(profile, k, v)

    user.save()

    profile.uid = uid
    profile.provider = provider
    profile.user = user
    profile.save()

    return profile
 
class OpenIdBackend:

    def authenticate(self, openid_key, request, provider, user=None):

        data = ProfileData()
        data.provider = provider

        if request.openid and request.openid.sreg:
            data.email = request.openid.sreg.get('email')
            data.user_name = request.openid.sreg.get('nickname')
            data.first_name, data.last_name = request.openid.sreg.get('fullname', ' ').split(' ', 1)
        elif request.openid and request.openid.ax:
            data.email = request.openid.ax.getSingle('http://axschema.org/contact/email')
            if 'Google' == provider:
                data.first_name = request.openid.ax.getSingle('http://axschema.org/namePerson/first')
                data.last_name = request.openid.ax.getSingle('http://axschema.org/namePerson/last')
            else:
                ax_schema = OPENID_AX_PROVIDER_MAP['Default']
                data.username = request.openid.ax.getSingle(ax_schema['nickname']) #should be replaced by correct schema
                data.first_name, data.last_name = request.openid.ax.getSingle(ax_schema['fullname']).split(' ', 1)

        return update_profile(request.user,provider,openid_key,data).user
  
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk = user_id)
            return user
        except User.DoesNotExist:
            return None

class LinkedInBackend:
    """LinkedInBackend for authentication"""
    def authenticate(self, linkedin_access_token, user=None):
        linkedin = LinkedIn(LINKEDIN_CONSUMER_KEY, LINKEDIN_CONSUMER_SECRET)
        # get their profile
        
        profile = ProfileApi(linkedin).getMyProfile(access_token = linkedin_access_token)

        data = ProfileData()
        data.first_name, data.last_name = profile.firstname, profile.lastname       
        data.token = linkedin_access_token

        return update_profile(user,"Linkedin",profile.id,data).user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None

class TwitterBackend:
    
    def authenticate(self, twitter_access_token, user=None):
        twitter = oauthtwitter.TwitterOAuthClient(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        try:
            userinfo = twitter.get_user_info(twitter_access_token)
        except:
            raise

        data = ProfileData()
        name_data = userinfo.name.split()
        data.username = userinfo.screen_name
        data.token = twitter_access_token

        try:
            data.first_name, data.last_name = name_data[0], ' '.join(name_data[1:])
        except:
            data.first_name, data.last_name = data.username, ''
 
        return update_profile(user,"Twitter",userinfo.id,data).user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None
        
class FacebookBackend:

    def authenticate(self, request, user=None):
        cookie = facebook.get_user_from_cookie(request.COOKIES, FACEBOOK_APP_ID, FACEBOOK_SECRET_KEY)
        if cookie:
            uid = cookie['uid']
            access_token = cookie['access_token']
        else:
            # if cookie does not exist
            # assume logging in normal way
            params = {}
            params["client_id"] = FACEBOOK_APP_ID
            params["client_secret"] = FACEBOOK_SECRET_KEY
            params["redirect_uri"] = request.build_absolute_uri(reverse("socialauth_facebook_login_done"))[:-1]
            params["code"] = request.GET.get('code', '')

            url = "https://graph.facebook.com/oauth/access_token?"+urllib.urlencode(params)
            from cgi import parse_qs
            userdata = urllib.urlopen(url).read()
            res_parse_qs = parse_qs(userdata)

            # Could be a bot query
            if not res_parse_qs.has_key('access_token'):
                return None

            access_token = res_parse_qs['access_token'][0]
            graph = facebook.GraphAPI(access_token) 
            fb_data = None
            try:
                fb_data = graph.get_object("me")
            except Exception, e:
                request.META['wsgi.errors'].write("Facebook API error: %s\n" % e )
                return None
                
            if not fb_data:
                return None

            request.META['wsgi.errors'].write("Facebook profile: %s ACCESS_TOKEN: %s\n" % ( fb_data, access_token ) )

            uid = fb_data['id']

        data = ProfileData()
        data.first_name = fb_data['first_name']
        data.last_name = fb_data['last_name']
        data.email = fb_data['email']
        data.token = access_token
 
        return update_profile(request.user,"Facebook",uid,data).user
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None
