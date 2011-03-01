from django.conf.urls.defaults import *

urlpatterns = patterns('bunch.views',
    url(r'^/(?P<id>\w+)$', 'bunch',name="bunch"),
)
