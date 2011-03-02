from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from models import Bunch

def bunch(request, path):
    return render_to_response('index.html', {'bunch':request.bunch }, context_instance=RequestContext(request) )
