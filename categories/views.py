from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.template.loader import select_template
from categories.models import Category
from video.models import Movie
from django.core.paginator import Paginator
from video.views import index
import settings


@cache_page(settings.CACHE_VIEW_LENGTH)
def category(request, path, with_stories=False, template_name='categories/category_detail.html', extra_context={}):

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
    
    templates = []
    while path_items:
        templates.append('categories/%s.html' % '_'.join(path_items))
        path_items.pop()
    templates.append(template_name)

    movies = Movie.objects.all().order_by( '-'+ request.sort )
    kwds = None
    if 'search' in request.GET:
        kwds = request.GET['search']
        keywords = kwds.split(' ')
        list_title_qs = [Q(title__icontains=x) for x in keywords]
        list_description_qs = [Q(description__icontains=x) for x in keywords]
        final_q = reduce(operator.or_, list_title_qs + list_description_qs)
        movies = movies.filter( final_q )
    paginator = Paginator(movies, 10 )

    context = RequestContext(request)
    context.update({'category':category, 'movies':paginator.page( request.page ) })
    if extra_context:
        context.update(extra_context)
    return HttpResponse(select_template(templates).render(context))
