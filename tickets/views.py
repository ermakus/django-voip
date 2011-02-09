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

from django import forms
from django.template.loader import render_to_string
import django.forms as forms

class SelectWithPop(forms.Select):
    def render(self, name, *args, **kwargs):
        html = super(SelectWithPop, self).render(name, *args, **kwargs)
        popupplus = render_to_string("tickets/popup_form.html", {'field': name})
        return html+popupplus

class EventForm(forms.ModelForm):
    class Meta:
        model = Event

class TicketForm(forms.ModelForm):
    event = forms.ModelChoiceField(Event.objects, widget=SelectWithPop) 
    class Meta:
        model = Ticket
        fields = ['event','count','price','comment']

def index(request):
    cats = Category.objects.all().filter( level=1 )
    return render_to_response( request.mutator + 'index.html', {'cats':cats }, context_instance=RequestContext(request))

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
def my(request):
    sell = Relation.objects.filter( user = request.user, role="BROKER" )
    buy = Relation.objects.filter( user = request.user, role="CUSTOMER" )
    return render_to_response('tickets/tickets.html', { 'sell':sell, 'buy':buy }, context_instance=RequestContext(request))

@login_required
def ticket(request, id):

    if ('action' in request.REQUEST) and (request.REQUEST['action'] == 'sell'):
        role = 'BROKER'
    else:
        role = 'CUSTOMER'

    event = None
    if 'event' in request.GET:
        event = request.GET['event']

    cat = None
    if 'cat' in request.GET:
        cat = request.GET['cat']

    try:
        instance = Ticket.objects.get( pk=id )
    except Ticket.DoesNotExist:
        instance = Ticket()

    form = TicketForm(request.POST or None, initial={'event':event }, instance=instance )

    if request.method == 'POST':
        if form.is_valid():
            ticket = form.save()
            if int(id) == 0:
                rel = Relation()
                rel.user = request.user
                rel.ticket = ticket
                rel.role = role
                rel.save()
            return HttpResponseRedirect( reverse( 'ticket_my' )  )

    return render_to_response( request.mutator + 'tickets/ticket.html', { 'form':form, 'id':id, 'role':role }, context_instance=RequestContext(request))

@login_required
def event(request,id):
    if request.method == 'POST':
        form = EventForm(request.POST)
    else:
        form = EventForm()
    return render_to_response( request.mutator + 'tickets/event.html', { 'form':form }, context_instance=RequestContext(request))

@login_required
def manage(request,id):
    ticket = get_object_or_404( Ticket, pk=id)
    return render_to_response( request.mutator + 'tickets/event.html', {  }, context_instance=RequestContext(request))
