import re

MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
IPAD_AGENT_RE=re.compile(r".*(ipad)",re.IGNORECASE)

class SiteMiddleware(object):
    def process_request(self, request):
        request.urlstate = '?'
        request.mutator=''

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
            request.urlstate =  '?'

        if 'page' in request.GET:
            request.page = request.GET['page']
        else:
            request.page = 1

        request.urlstate += ("page=%s&" % request.page )

        if 'sort' in request.GET:
            request.sort = request.GET['sort']
        else:
            request.sort = 'rating'

        request.urlstate += ("sort=%s&" % request.sort )

        if request.path.find('categories') != -1:
            request.category = request.path.strip('/')[11:]
        else:
            request.category = 'root'

        return None

