from django.contrib import admin
from models import *

class EventAdmin(admin.ModelAdmin):
    filter_horizontal = ['cats',]

admin.site.register( Event, EventAdmin )
admin.site.register( Ticket )
admin.site.register( Relation )
