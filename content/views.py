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

    return render_to_response('content/upload.html', opts, context_instance=RequestContext(request))

