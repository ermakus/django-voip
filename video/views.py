# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.comments.models import Comment
from models import *
from django.template import Library, RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.views.decorators.cache import cache_page
from settings import CACHE_VIEW_LENGTH
from categories.models import Category

import settings, operator

def index(request):
    cats = Category.objects.all().filter( level=1 )
    return render_to_response( request.mutator + 'index.html', {'cats':cats }, context_instance=RequestContext(request))

def script(request):
   return render_to_response('common.js', { }, context_instance=RequestContext(request))

def context(request):
    if request.user.is_authenticated():
        relations = MovieRelation.objects.filter( user = request.user )
        return HttpResponse('{"user":"%s","bag":"%s"}' % ( request.user.username, relations.count() ), mimetype="text/json" )
    else:
        return HttpResponse("false", mimetype="text/json" )

@cache_page( CACHE_VIEW_LENGTH )
def feed(request,type,page):
    movies = Movie.objects.all().order_by( '-'+type );
    paginator = Paginator(movies, settings.PAGINATION)
    return render_to_response('feed.html', { 'movies':paginator.page( page ), 'type':type }, context_instance=RequestContext(request))

def bag_view(request,page):
    relations = MovieRelation.objects.filter( user = request.user )
    paginator = Paginator(relations, settings.PAGINATION)
    return render_to_response('bag_view.html', { 'relations':paginator.page( page ) }, context_instance=RequestContext(request))

def movie(request, movie_id ):
    movie = get_object_or_404(Movie, pk=movie_id)
    movie.views = movie.views + 1
    movie.save()
    purchased = "No"
    if request.user.is_authenticated():
        relations = MovieRelation.objects.filter( user = request.user, movie = movie )
	if len(relations) > 0:
            purchased = "Yes"
        
    return render_to_response( request.mutator + 'movie.html', { 'movie':movie, 'purchased':purchased }, context_instance=RequestContext(request))

@cache_page( CACHE_VIEW_LENGTH )
def gallery(request, page, type ):
    movies = Movie.objects.all().order_by( '-'+type )
    kwds = None
    if 'search' in request.GET:
        kwds = request.GET['search']
	keywords = kwds.split(' ')
        list_title_qs = [Q(title__icontains=x) for x in keywords]  
        list_description_qs = [Q(description__icontains=x) for x in keywords]  
        final_q = reduce(operator.or_, list_title_qs + list_description_qs)  
        movies = movies.filter( final_q )
    paginator = Paginator(movies, settings.PAGINATION)
    return render_to_response( request.mutator + 'gallery.html', { 'movies':paginator.page( page ), 'search':kwds, 'type':type }, context_instance=RequestContext(request))

@login_required
def buy(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    rel = None
    if 'code' in request.GET:
        rel = movie.add_relation('buy', request.user, '')
    return render_to_response('buy.html', { 'movie':movie,'rel':rel }, context_instance=RequestContext(request))

@login_required
def bag(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    rel = movie.add_relation('bag', request.user, '')
    return render_to_response('bag.html', { 'movie':movie }, context_instance=RequestContext(request))

@login_required
def bag_drop(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    movie.del_relation( 'bag', request.user )
    movie.del_relation( 'buy', request.user )
    return HttpResponse("OK")
