#CORE
import datetime

#THIRD PARTY
from django.conf import settings
from django.db import models

#LOCAL
from djangae.contrib.gauth.models import GaeUser


class PublicPostManager(models.Manager):
    """
    Custom manager to only return 'public' posts, i.e those that have a 
    'public' version, and whose 'published' date is in the past (future dates *should* 
    be handled by the class based views)
    """
    def get_queryset(self):
        if False: #TODO if user is authenticated and marked as author
            #return everything
            return super(PublicPostManager, self).get_queryset()
        else:
            #return only public visible posts
            return super(PublicPostManager, self).get_queryset().filter(public=True)


class BlogPost(models.Model):
    """
    top level BlogPost object to connect a google user (author) to a set 
    of BlogPostVersions. 
    """

    #fields
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,null=True)


class BlogPostVersion(models.Model):
    """
    A version of a BlogPost. A BlogPost may have any number of 
    BlogPostVersions, but only one of these may be 'public' at any
    time. A BlogPost without a public version should not be visible on
    the site.
    """
    objects = PublicPostManager()
    visible = PublicPostManager()

    blog = models.ForeignKey(BlogPost, related_name='versions')
    
    copy = models.TextField()
    public = models.BooleanField(default=False)
    published = models.DateTimeField(default=datetime.datetime.now())
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    copy = models.TextField()