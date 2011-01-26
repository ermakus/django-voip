from django.conf.urls.defaults import *
from categories.models import Category

categorytree_dict = {
}

urlpatterns = patterns('categories.views',
    url(r'^$', 'catalog', name='catalog'),
    url(r'^(?P<path>.+)/$', 'category', name='category'),
)
