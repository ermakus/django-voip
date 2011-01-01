from models import *
from django.contrib import admin

class MovieAttributeInline(admin.TabularInline):
    model = MovieAttribute

class MovieAdmin(admin.ModelAdmin):
    inlines = [ MovieAttributeInline, ]

admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieRelation)
admin.site.register(FriendRelation)

