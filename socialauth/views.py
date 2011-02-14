import logging
import urllib
from oauth import oauth

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout

from openid_consumer.views import begin
from socialauth.lib import oauthtwitter2 as oauthtwitter
from django.contrib.auth.forms import AuthenticationForm
                           
from socialauth.lib.linkedin import *

LINKEDIN_CONSUMER_KEY = getattr(settings, 'LINKEDIN_CONSUMER_KEY', '')
LINKEDIN_CONSUMER_SECRET = getattr(settings, 'LINKEDIN_CONSUMER_SECRET', '')

ADD_LOGIN_REDIRECT_URL = getattr(settings, 'ADD_LOGIN_REDIRECT_URL', '')
LOGIN_REDIRECT_URL = getattr(settings, 'LOGIN_REDIRECT_URL', '')
LOGIN_URL = getattr(settings, 'LOGIN_URL', '')

TWITTER_CONSUMER_KEY = getattr(settings, 'TWITTER_CONSUMER_KEY', '')
TWITTER_CONSUMER_SECRET = getattr(settings, 'TWITTER_CONSUMER_SECRET', '')

FACEBOOK_APP_ID = getattr(settings, 'FACEBOOK_APP_ID', '')
FACEBOOK_API_KEY = getattr(settings, 'FACEBOOK_API_KEY', '')
FACEBOOK_SECRET_KEY = getattr(settings, 'FACEBOOK_SECRET_KEY', '')


def del_dict_key(src_dict, key):
    if key in src_dict:
        del src_dict[key]

def set_next(request, embed=False):
    next_url = LOGIN_REDIRECT_URL
    if 'next' in request.REQUEST:
        next_url = request.REQUEST['next']
    if not embed:
        next_url = next_url.replace('embed=yes','')
    request.session['login_next'] = next_url
    return next_url

def login_page(request):
    error = False
    if  request.method == "POST":
        error = "Invalid login or password"
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Okay, security checks complete. Log the user in.
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(request.session['login_next'])

    request.session.set_test_cookie()
    return render_to_response('socialauth/login_page.html', {
	'next': set_next( request, embed=True ),
	'error': error,
    }, context_instance=RequestContext(request))


def render_error(request, error):
    return render_to_response('socialauth/login_page.html', {
	'next' : request.session['login_next'] or LOGIN_REDIRECT_URL,
	'error': error,
    }, context_instance=RequestContext(request))
 
def linkedin_login(request):
    set_next(request)
    linkedin = LinkedIn(LINKEDIN_CONSUMER_KEY, LINKEDIN_CONSUMER_SECRET)
    request_token = linkedin.getRequestToken(callback = request.build_absolute_uri(reverse('socialauth_linkedin_login_done')))
    request.session['linkedin_request_token'] = request_token
    signin_url = linkedin.getAuthorizeUrl(request_token)
    return HttpResponseRedirect(signin_url)

def linkedin_login_done(request):
    request_token = request.session.get('linkedin_request_token', None)

    if not request_token:
        return render_error(request,'No request token in session')

    try:
        linkedin = LinkedIn(settings.LINKEDIN_CONSUMER_KEY, settings.LINKEDIN_CONSUMER_SECRET)
        verifier = request.GET.get('oauth_verifier', None)
        access_token = linkedin.getAccessToken(request_token,verifier)
        request.session['access_token'] = access_token
        user = authenticate(linkedin_access_token=access_token, request=request, user=request.user )
        login(request, user)
    except Exception, e:
         del_dict_key(request.session, 'access_token')
         del_dict_key(request.session, 'request_token')
         return render_error( request, "System error: %s" % e )

    return HttpResponseRedirect(request.session['login_next'])

def twitter_login(request):
    set_next(request)
    twitter = oauthtwitter.TwitterOAuthClient(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    request_token = twitter.fetch_request_token(callback = request.build_absolute_uri(reverse('socialauth_twitter_login_done')))
    request.session['request_token'] = request_token.to_string()
    signin_url = twitter.authorize_token_url(request_token)
    return HttpResponseRedirect(signin_url)

def twitter_login_done(request):
    request_token = request.session.get('request_token', None)
    verifier = request.GET.get('oauth_verifier', None)
    denied = request.GET.get('denied', None)
    
    if denied:
        return render_error(request,'Access denied')

    if not request_token:
        return render_error(request,'No request token in session')

    token = oauth.OAuthToken.from_string(request_token)

    if token.key != request.GET.get('oauth_token', 'no-token'):
        del_dict_key(request.session, 'request_token')
        return render_error(request,'Invalid request token')

    try:
        twitter = oauthtwitter.TwitterOAuthClient(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        access_token = twitter.fetch_access_token(token, verifier)
        request.session['access_token'] = access_token.to_string()
        user = authenticate(twitter_access_token=access_token, request=request, user=request.user)
        login(request, user)
    except Exception, e:
        raise
        del_dict_key(request.session, 'access_token')
        del_dict_key(request.session, 'request_token')
        return render_error(request,'System error: %s' % e)

    return HttpResponseRedirect(request.session['login_next'])

def openid_login(request):
    if request.method == 'POST':
        return login_page(request)

    set_next( request )
    if 'openid_identifier' in request.GET:
        user_url = request.GET.get('openid_identifier')
        request.session['openid_provider'] = user_url
        return begin(request, user_url = user_url)
    else:
        request.session['openid_provider'] = 'Openid'
        return begin(request)

def google_login(request):
    set_next( request )
    request.session['openid_provider'] = 'Google'
    return begin(request, user_url='https://www.google.com/accounts/o8/id')

def yahoo_login(request):
    request.session['openid_provider'] = 'Yahoo'
    return begin(request, user_url='https://me.yahoo.com/')

def openid_done(request, provider=None):

    if not provider:
        provider = request.session.get('openid_provider', '')

    if hasattr(request,'openid') and request.openid:
        try:
            openid_key = str(request.openid)
            user = authenticate(openid_key=openid_key, request=request, provider=provider)
            login(request, user)
            return HttpResponseRedirect(request.session['login_next'])

        except Exception, e:
            return render_error( request, "System error: %s" % e )

    return render_error( request, "Invalid request" )

def facebook_login(request):
    set_next( request )
    if request.REQUEST.get("device"):
        device = request.REQUEST.get("device")
    else:
        device = "user-agent"

    params = {}
    params["client_id"] = FACEBOOK_APP_ID
    params["redirect_uri"] = request.build_absolute_uri(reverse("socialauth_facebook_login_done"))[:-1]
    params["scope"] = "user_about_me,user_activities,user_relationships,email,publish_stream,user_location,user_birthday,user_photos"
    url = "https://graph.facebook.com/oauth/authorize?"+urllib.urlencode(params)

    return HttpResponseRedirect(url)

def facebook_login_done(request):
    user = authenticate(request=request)
    if not user:
        request.COOKIES.pop(FACEBOOK_API_KEY + '_session_key', None)
        request.COOKIES.pop(FACEBOOK_API_KEY + '_user', None)

        # TODO: maybe the project has its own login page?
        logging.debug("SOCIALAUTH: Couldn't authenticate user with Django, redirecting to Login page")
        return HttpResponseRedirect(reverse('socialauth_login_page'))

    login(request, user)
    
    return HttpResponseRedirect(request.session['login_next'])

def logout(request, next_page=None, template_name='registration/logged_out.html'):
    "Logs out the user and displays 'You are logged out' message."
    from django.contrib.auth import logout
    logout(request)
    if next_page is None:
        return render_to_response(template_name, {'title': 'Logged out'}, context_instance=RequestContext(request))
    else:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page or request.path)

def social_logout(request):
    # Todo
    # still need to handle FB cookies, session etc.

    # let the openid_consumer app handle openid-related cleanup
    from openid_consumer.views import signout as oid_signout
    oid_signout(request)

    # normal logout
    logout_response = logout(request)
    
    if 'next' in request.GET:
        return HttpResponseRedirect(request.GET.get('next'))
    elif getattr(settings, 'LOGOUT_REDIRECT_URL', None):
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
    else:
        return logout_response

