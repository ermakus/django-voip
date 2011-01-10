from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'video.views.index'),
    (r'^video/', include('video.urls')), 
    (r'^social/', include('socialauth.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^admin/', admin.site.urls), 
    (r'^categories/', include('categories.urls')),
    (r'^uploadify/', include('uploadify.urls')),
)


#from django.conf import settings
#if settings.DEBUG:
    
#    urlpatterns += patterns('',
        # This is for the CSS and static files:
#        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': settings.MEDIA_ROOT, 'show_indexes':True }),
#    )
    
