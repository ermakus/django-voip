from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
import facebook
from django.contrib.auth import authenticate, login
import urllib, urllib2
from socialauth.lib import oauthtwitter2 as oauthtwitter
from socialauth.models import Profile
from socialauth.lib.linkedin import *
from asterisk.models import Channel

import random, unicodedata, string

TWITTER_CONSUMER_KEY = getattr(settings, 'TWITTER_CONSUMER_KEY', '')
TWITTER_CONSUMER_SECRET = getattr(settings, 'TWITTER_CONSUMER_SECRET', '')

FACEBOOK_APP_ID = getattr(settings, 'FACEBOOK_APP_ID', '')
FACEBOOK_API_KEY = getattr(settings, 'FACEBOOK_API_KEY', '')
FACEBOOK_SECRET_KEY = getattr(settings, 'FACEBOOK_SECRET_KEY', '')

LINKEDIN_CONSUMER_KEY = getattr(settings, 'LINKEDIN_CONSUMER_KEY', '')
LINKEDIN_CONSUMER_SECRET = getattr(settings, 'LINKEDIN_CONSUMER_SECRET', '')

OPENID_AX_PROVIDER_MAP = getattr(settings, 'OPENID_AX_PROVIDER_MAP', {})

            
def LOG_ERROR(request,msg):
    request.META['wsgi.errors'].write( msg )

def make_username(full_name):
        
    name = unicodedata.normalize('NFKD', unicode(full_name.lower())).encode('ASCII', 'ignore')
    name = name.split(' ')
    lastname = name[-1]
    firstname = name[0]
    
    username = '%s%s' % (firstname[0], lastname)
    if User.objects.filter(username=username).count() > 0:
        username = '%s%s' % (firstname, lastname[0])
        if User.objects.filter(username=username).count() > 0:
            users = User.objects.filter(username__regex=r'^%s[1-9]{1,}$' % firstname).order_by('username').values('username')                
            if len(users) > 0:
                last_number_used = map(lambda x: int(x['username'].replace(firstname,'')), users)
                last_number_used.sort()
                last_number_used = last_number_used[-1]
                number = last_number_used + 1
                username = '%s%s' % (firstname, number)
            else:
                username = '%s%s' % (firstname, 1)
    
    return username

def make_channel():
    ch = ''.join([random.choice('0123456789') for i in xrange(4)])
    while True:
        try:
            Channel.objects.get( name = ch )
        except Channel.DoesNotExist:
            return ch

def make_password():
    return ''.join([random.choice(string.letters + string.digits) for i in xrange(8)])

class ProfileData(object):
    pass

def update_profile(request,provider,uid,data):

    def def_val(name, val):
        if not hasattr(data,name) or getattr(data,name) is None:
             setattr(data,name,val)
    profile = None
    user = request.user
    try:
        profile = Profile.objects.get(uid = uid)
        user = profile.user
        user.backend='django.contrib.auth.backends.ModelBackend'
        login( request, user )
    except Profile.DoesNotExist:
	profile = Profile()
        pass
 
    if not user or not user.is_authenticated():
        user = User()
    else:
        user = User.objects.get( username=user.username )

    def_val('first_name', "")
    def_val('last_name', "")

    fullname = ("%s %s" % (data.first_name, data.last_name)).strip()

    if hasattr(data,"username"):
        data.username = make_username( data.username )
    else:
        def_val('username', make_username( fullname or "user") )

    def_val('email', data.username + "@cloudpub.us" )
    data.provider = provider

    for k,v in data.__dict__.iteritems():
        setattr(user, k, v)
        setattr(profile, k, v)

    user.save()

    profile.uid = uid
    profile.provider = provider
    profile.user = user
    profile.save()

    try:
        channel = Channel.objects.get( user = user )
    except Channel.DoesNotExist:
        channel = Channel( user=user )
        channel.name = make_channel()
        channel.secret = make_password()
        channel.callerid = fullname
        channel.save()

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

        return update_profile(request,provider,openid_key,data).user
  
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk = user_id)
            return user
        except User.DoesNotExist:
            return None

class LinkedInBackend:
    """LinkedInBackend for authentication"""
    def authenticate(self, linkedin_access_token, request, user=None):
        linkedin = LinkedIn(LINKEDIN_CONSUMER_KEY, LINKEDIN_CONSUMER_SECRET)
        # get their profile
        
        profile = ProfileApi(linkedin).getMyProfile(access_token = linkedin_access_token)

        data = ProfileData()
        data.first_name, data.last_name = profile.firstname, profile.lastname       
        data.token = linkedin_access_token

        return update_profile(request,"Linkedin",profile.id,data).user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None

class TwitterBackend:
    
    def authenticate(self, twitter_access_token, request, user=None):
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
 
        return update_profile(request,"Twitter",userinfo.id,data).user

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
            userdata = urllib2.urlopen(url).read()
            res_parse_qs = parse_qs(userdata)

            # Could be a bot query
            if not res_parse_qs.has_key('access_token'):
                return None

            access_token = res_parse_qs['access_token'][0]
            graph = facebook.GraphAPI(access_token) 
            fb_data = graph.get_object("me")
                
            if not fb_data:
                raise Exception("Error capturing facebook profile")

            uid = fb_data['id']

        data = ProfileData()
        data.first_name = fb_data['first_name']
        data.last_name = fb_data['last_name']
        data.email = fb_data['email']
        data.token = access_token
 
        return update_profile(request,"Facebook",uid,data).user
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None
