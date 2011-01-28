from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'content.views.index'),
    (r'^content/', include('content.urls')), 
    (r'^social/', include('socialauth.urls')),
    (r'^accounts/', include('userprofile.urls')),
    (r'^admin/', admin.site.urls), 
    (r'^categories/', include('categories.urls')),
    url(r'^preview/(?P<page_id>\d+)/', 'feincms.views.base.preview_handler', name='feincms:preview'),
    url(r'^(.*)/$|^$', 'feincms.views.applicationcontent.handler'),
)


#from django.conf import settings
#if settings.DEBUG:
    
#    urlpatterns += patterns('',
        # This is for the CSS and static files:
#        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': settings.MEDIA_ROOT, 'show_indexes':True }),
#    )
    
