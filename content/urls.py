from django.conf.urls.defaults import *

urlpatterns = patterns('content.views',
    url(r'^upload$', 'upload', name='upload'),
)
