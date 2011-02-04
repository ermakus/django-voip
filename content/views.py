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
from django.views.decorators.csrf import csrf_exempt
from backends import S3
from django.core.urlresolvers import reverse

import settings, operator, base64

def index(request):
    cats = Category.objects.all().filter( level=1 )
    return render_to_response( request.mutator + 'index.html', {'cats':cats }, context_instance=RequestContext(request))

def script(request):
   return render_to_response('common.js', { }, context_instance=RequestContext(request))

@login_required
def upload(request):

    filename = 'test_upload';
    MAX_FILE_SIZE = 50 * 1048576;
    expiration = "2012-01-01T00:00:00Z"
    is_mac = False
    success_timeout = 0
    if is_mac: success_timeout = 5

    success_url=reverse('upload')

    policy = '''{
        "expiration": "%s",
        "conditions": [
        {"bucket": "%s"},
        ["starts-with", "$key","%s"],
        {"acl": "public-read"},
        ["content-length-range", 0, %s],
        {"success_action_status": "201"},
        ["starts-with", "$Filename", ""], 
        ["starts-with", "$Content-Type", "image/"]
    ]}'''.replace("\n","") % ( expiration, settings.AWS_STORAGE_BUCKET_NAME, filename, MAX_FILE_SIZE, ) ;

    policy = base64.encodestring(policy).replace("\n","")

    opts = { 'is_mac':is_mac, 
             'success_url':success_url, 
             'success_timeout':success_timeout, 
	     'access_key':settings.AWS_ACCESS_KEY_ID, 
             'bucket':settings.AWS_STORAGE_BUCKET_NAME, 
             'filename':filename,
	     'max_size':MAX_FILE_SIZE,
	     'policy':policy,
	     'signature':S3.encode( settings.AWS_SECRET_ACCESS_KEY, policy )  }

    return render_to_response('upload.html', opts, context_instance=RequestContext(request))


def context(request):
    if request.user.is_authenticated():
        relations = Relation.objects.filter( user = request.user )
	username = request.user.first_name + " " + request.user.last_name
	if username.strip() == "":
	    username = request.user.email
       	if username.strip() == "":
	    username = request.user.username
        return HttpResponse('{"user":"%s","count":"%s"}' % ( username , relations.count() ), mimetype="text/json" )
    else:
        return HttpResponse("false", mimetype="text/json" )

@login_required
def private(request,page):
    relations = Relation.objects.filter( user = request.user )
    paginator = Paginator(relations, settings.PAGINATION)
    return render_to_response('private.html', { 'relations':paginator.page( page ) }, context_instance=RequestContext(request))

def content(request, content_id ):
    movie = get_object_or_404(Entry, pk=content_id)
    movie.views = movie.views + 1
    movie.save()
    purchased = "No"
    if request.user.is_authenticated():
        relations = Relation.objects.filter( user = request.user, movie = movie )
	if len(relations) > 0:
            purchased = "Yes"
        
    return render_to_response( request.mutator + 'content.html', { 'movie':movie, 'purchased':purchased }, context_instance=RequestContext(request))

@login_required
def buy(request, content_id):
    content = get_object_or_404(Movie, pk=content_id)
    rel = None
    if 'code' in request.GET:
        rel = content.add_relation('buy', request.user, '')
    return render_to_response('buy.html', { 'content':content,'rel':rel }, context_instance=RequestContext(request))
