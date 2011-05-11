from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.template.loader import select_template
from categories.models import Category
from django.core.paginator import Paginator
from django.db.models import Q
from socialauth.models import Profile

import operator
import settings

def get_category( path ):
    path_items = path.strip('/').split('/')

    if len(path_items) >= 2:
        return get_object_or_404(Category,
            slug__iexact = path_items[-1],
            level = len(path_items)-1,
            parent__slug__iexact=path_items[-2])
    else:
        return get_object_or_404(Category,
            slug__iexact = path_items[-1],
            level = len(path_items)-1)


def catalog(request):
    category = get_category( "/root" )
    return render_to_response('categories/catalog.html', {'category':category }, context_instance=RequestContext(request))

#@cache_page(settings.CACHE_VIEW_LENGTH)
def category(request, path):
    category = get_category( path )
    profiles = Profile.objects.filter(categories__id = category.pk)
    search = kwds = None
    if 'search' in request.GET:
        search = kwds = request.GET['search']
        keywords = kwds.split(' ')
        list_fn_qs = [Q(first_name__icontains=x) for x in keywords]
        list_ln_qs = [Q(last_name__icontains=x) for x in keywords]
        final_q = reduce(operator.or_, list_fn_qs + list_ln_qs)
        profiles = profiles.filter( final_q )

    return render_to_response('categories/category.html', {'category':category, 'profiles':profiles, 'search':search }, context_instance=RequestContext(request) )

                                                                        
