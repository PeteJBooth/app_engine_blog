from django.views.generic import ArchiveIndexView
from google.appengine.api import users

from .models import BlogPost,BlogPostVersion

class GauthMixin(object):
    def get_context_data(self, **kwargs):
        context = super(GauthMixin,self).get_context_data(**kwargs)
        user = users.get_current_user()

        if user:
            context['user_authenticated'] = True
            context['user_nick'] = user.nickname()
        else:
            context['user_authenticated'] = False
        #TODO- stick this in a context processor
        context['logout_url']  = users.create_logout_url('/')
        context['login_url'] = users.create_login_url('/')
        return context


class BlogIndexView(GauthMixin, ArchiveIndexView):
    allow_empty = True
    #because the datastore can't do joins I'm going to use the version model
    #to pull back the posts
    model = BlogPostVersion
    date_field = 'published'
