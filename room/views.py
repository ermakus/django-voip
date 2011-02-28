from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.comments.models import Comment
from models import *
from django.template import Library, RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.views.decorators.cache import cache_page
from categories.models import Category
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django import forms
from django.template.loader import render_to_string
import django.forms as forms
from asterisk.models import Channel

def index(request):
    cats = Category.objects.all().filter( level=1 )
    rooms = Room.objects.all().order_by('rating')[:10]
    return render_to_response( request.mutator + 'index.html', {'cats':cats,'rooms':rooms }, context_instance=RequestContext(request))

def context(request):
    if request.user.is_authenticated():
	username = request.user.first_name + " " + request.user.last_name
	if username.strip() == "":
	    username = request.user.email
       	if username.strip() == "":
	    username = request.user.username
        return HttpResponse('{"user":"%s"}' % ( username ), mimetype="text/json" )
    else:
        return HttpResponse("false", mimetype="text/json" )

@login_required
def rooms_view(request):
    rooms = Room.objects.filter( moderator = request.user )
    return render_to_response('room/rooms.html', { 'rooms':rooms }, context_instance=RequestContext(request))

@login_required
def call_view(request):
    channel = get_object_or_404(Channel,user=request.user)
    try:
        site = Site.objects.get_current()
    except:
        site = Site(domain='localhost')
    return render_to_response( request.mutator + 'room/call.html', { 'site':site, 'channel':channel }, context_instance=RequestContext(request))

@login_required
def chat_view(request, id):
    try:
        room = Room.objects.get( pk=id )
    except Room.DoesNotExist:
        room = Room()

    channel = get_object_or_404(Channel,user=request.user)
    try:
        site = Site.objects.get_current()
    except:
        site = Site(domain='localhost')
    return render_to_response( request.mutator + 'room/chat.html', { 'site':site, 'room':room, 'channel':channel }, context_instance=RequestContext(request))


@login_required
def room_view(request, id):

    try:
        room = Room.objects.get( pk=id )
    except Room.DoesNotExist:
        room = Room()

    channel = get_object_or_404(Channel,user=request.user)
    try:
        site = Site.objects.get_current()
    except:
        site = Site(domain='localhost')
    return render_to_response( request.mutator + 'room/room.html', { 'site':site, 'room':room, 'channel':channel }, context_instance=RequestContext(request))

def update_object(request,instance):
    instance.content_type = "text/plain"
    instance.message = request.POST['message']
    return

def delete_object(request,instance):
    instance.content_type = "text/plain"
    instance.message = request.POST['message']
    return


ACTIONS={ 'update':update_object, 'delete':update_object }

@login_required
@csrf_exempt
def snippet(request,id,action):
    try:
        instance = Snippet.objects.get( uid=uid )
    except Stream.DoesNotExist:
        instance = Snippet()
        instance.user = request.user
    if action in ACTIONS:
        ACTIONS[action]( instance )
    instance.state=action
    instance.save()
    return HttpResponse("true")
