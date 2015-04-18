#CORE
from django.conf.urls import patterns, include, url

#LOCAL
from .views import BlogIndexView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'scaffold.views.home', name='home'),
    url(r'^$', BlogIndexView.as_view(), name='index'),
)
