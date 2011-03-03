from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
#    (r'^$', 'bunch.views.bunch',{'path':'/'}),
    (r'^room/', include('room.urls')), 
    (r'^bunch/', include('bunch.urls')), 
    (r'^social/', include('socialauth.urls')),
    (r'^accounts/', include('userprofile.urls')),
    (r'^admin/', admin.site.urls), 
    (r'^categories/', include('categories.urls')),
    (r'^schedule/', include('schedule.urls')),
    url(r'^(?P<path>.+)$', 'bunch.views.bunch', name="bunch"),
)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': settings.MEDIA_ROOT, 'show_indexes':True }),
    )
    
