import re
from models import Bunch

MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
IPAD_AGENT_RE=re.compile(r".*(ipad)",re.IGNORECASE)

class BunchMiddleware(object):
    def process_request(self, request):

        if not request.path or request.path == '/': request.path ='/god'
 

        try:
            request.bunch = Bunch.resolve( request.path )
        except Bunch.DoesNotExist:
            request.bunch = Bunch(uid='error',kind='error',content='Path not exists: %s' % request.path )

        browser = "Unknown"
        if 'HTTP_USER_AGENT' is request.META:
            browser = request.META['HTTP_USER_AGENT']

        if not IPAD_AGENT_RE.match(browser) and MOBILE_AGENT_RE.match(browser):
            request.template = 'mobile/site.html'
        else:
            request.template = 'site.html'

        if 'embed' in request.REQUEST:
            request.kind  = request.REQUEST['embed']
            request.urlstate =  '?embed=' + request.kind
            request.template = 'embed.html'
        else:
            request.kind = 'html'
            request.urlstate =  ''

        return None
