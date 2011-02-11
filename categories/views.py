from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.template.loader import select_template
from categories.models import Category
from django.core.paginator import Paginator
from django.db.models import Q
from room.models import *
import operator
import settings

def catalog(request):
    render_to_response('categories/catalog.html')

#@cache_page(settings.CACHE_VIEW_LENGTH)
def category(request, path):

    path_items = path.strip('/').split('/')

    if len(path_items) >= 2:
        category = get_object_or_404(Category,
            slug__iexact = path_items[-1],
            level = len(path_items)-1,
            parent__slug__iexact=path_items[-2])
    else:
        category = get_object_or_404(Category,
            slug__iexact = path_items[-1],
            level = len(path_items)-1)

    rooms = Room.objects.all().order_by( '-'+ request.sort )
    kwds = None
    if 'search' in request.GET:
        kwds = request.GET['search']
        keywords = kwds.split(' ')
        list_title_qs = [Q(title__icontains=x) for x in keywords]
        list_more_qs = [Q(more__icontains=x) for x in keywords]
        final_q = reduce(operator.or_, list_title_qs + list_more_qs)
        rooms = events.filter( final_q )

    return render_to_response('categories/category.html', {'category':category, 'rooms':rooms }, context_instance=RequestContext(request) )
