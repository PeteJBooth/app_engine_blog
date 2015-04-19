#CORE
from django.conf.urls import patterns, include, url

#LOCAL
from .views import BlogPostIndexView,BlogPostDetailView, BlogPostAddView, BlogPostYearView,BlogPostMonthView,BlogPostDayView

urlpatterns = patterns('blog.views',
    # Examples:
    # url(r'^$', 'scaffold.views.home', name='home'),
    url(r'^$', BlogPostIndexView.as_view(), name='index'),
    url(r'^posts/(?P<slug>[\w-]+)/', BlogPostDetailView.as_view(), name='post_detail'),
    url(r'^(?P<year>[0-9]{4})/$', BlogPostYearView.as_view(), name='post_year'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', BlogPostMonthView.as_view(), name='post_month'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', BlogPostDayView.as_view(), name='post_day'),
    url(r'^add/$', BlogPostAddView.as_view(), name='post_add'),
)
