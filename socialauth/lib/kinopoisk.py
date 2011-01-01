import hashlib
import urllib2
import httplib

import time


import oauth.oauth as oauth

class Kinopoisk():
    KP_SERVER = "www.kinopoisk.ru"
    KP_API_URL = "http://www.kinopoisk.ru/api"

    REQUEST_TOKEN_URL = KP_API_URL + "/oauth/request_token"
    AUTHORIZE_URL = KP_API_URL + "/oauth/authorize"
    ACCESS_TOKEN_URL = KP_API_URL + "/oauth/access_token"


    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.connection = httplib.HTTPConnection(self.KP_SERVER)
        self.consumer = oauth.OAuthConsumer(api_key, secret_key)
        self.sig_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        self.profile_api = KinopoiskProfileApi(self)

    def getRequestToken(self, callback):
        oauth_consumer_key = self.api_key

        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer,
                        callback=callback,
                        http_url = self.REQUEST_TOKEN_URL)
        oauth_request.sign_request(self.sig_method, self.consumer, None)


        self.connection.request(oauth_request.http_method,
                        self.REQUEST_TOKEN_URL, headers = oauth_request.to_header())
        response = self.connection.getresponse().read()
        
        token = oauth.OAuthToken.from_string(response)
        return token

    def getAuthorizeUrl(self, token):
        """
        Get the URL that we can redirect the user to for authorization of our
        application.
        """
        oauth_request = oauth.OAuthRequest.from_token_and_callback(token=token, http_url = self.AUTHORIZE_URL)
        return oauth_request.to_url()

    def getAccessToken(self, token, verifier):
        """
        Using the verifier we obtained through the user's authorization of
        our application, get an access code.

        Note: token is the request token returned from the call to getRequestToken

        @return an OAuthToken object with the access token.  Use it like this:
                token.key -> Key
                token.secret -> Secret Key
        """
        token.verifier = verifier
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=token, verifier=verifier, http_url=self.ACCESS_TOKEN_URL)
        oauth_request.sign_request(self.sig_method, self.consumer, token)
        
        # self.connection.request(oauth_request.http_method, self.ACCESS_TOKEN_URL, headers=oauth_request.to_header()) 
        self.connection.request(oauth_request.http_method, oauth_request.to_url()) 
        response = self.connection.getresponse().read()
        return oauth.OAuthToken.from_string(response)

    """
    More functionality coming soon...
    """

class KinopoiskApi():
    def __init__(self, kp):
        self.kp = kp

    def doApiRequest(self, url, access_token):
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.kp.consumer, token=access_token, http_url=url)
        oauth_request.sign_request(self.kp.sig_method, self.kp.consumer, access_token)
        print "OUath request: %s" % oauth_request.to_url()
        self.kp.connection.request("GET", oauth_request.to_url())
        return self.kp.connection.getresponse().read()


class KinopoiskProfileApi(KinopoiskApi):
    STATUS_SELF_URL = Kinopoisk.KP_API_URL + "/provider/profile"
    
    def __init__(self, kp):
        KinopoiskApi.__init__(self, kp)
    
    def getMyProfile(self, access_token):
        return self.doApiRequest(self.STATUS_SELF_URL, access_token)
