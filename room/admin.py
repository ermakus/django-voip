from django.contrib import admin
from models import *

class RoomAdmin(admin.ModelAdmin):
    filter_horizontal = ['cats',]

admin.site.register( Room, RoomAdmin )
admin.site.register( Meeting )
admin.site.register( Stream )
