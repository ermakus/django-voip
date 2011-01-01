from models import MovieRelation
import re
MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

class VideoMiddleware(object):
    def process_request(self, request):
        request.urlstate = '?'

        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            request.mutator=''#'mobile/'
        else:
            request.mutator=''

        if 'embed' in request.GET:
            request.template = 'embed.html'
            request.urlstate +=  'embed=yes&'
        else:
            request.template = 'site.html'

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

        if request.user.is_authenticated():
            rels = MovieRelation.objects.filter( user = request.user )
            request.bag_count = rels.count()
        return None

