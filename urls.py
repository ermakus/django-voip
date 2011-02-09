from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'tickets.views.index'),
    (r'^tickets/', include('tickets.urls')), 
    (r'^social/', include('socialauth.urls')),
    (r'^accounts/', include('userprofile.urls')),
    (r'^admin/', admin.site.urls), 
    (r'^categories/', include('categories.urls')),
)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': settings.MEDIA_ROOT, 'show_indexes':True }),
    )
    
