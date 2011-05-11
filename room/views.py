from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.comments.models import Comment
from models import *
from django.template import Library, RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from asterisk.models import Channel
from socialauth.models import Profile 


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

def profiles(request,category):
    profiles = Profile.objects.filter(categories__id = category)
    return render_to_response('profiles.html', { 'profiles':profiles }, context_instance=RequestContext(request))

