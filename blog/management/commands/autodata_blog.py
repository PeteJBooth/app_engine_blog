import datetime

from django.core import management
from django.core.management.base import NoArgsCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.webdesign.lorem_ipsum import paragraphs,sentence


from blog.models import BlogPost, BlogPostVersion

class Command(NoArgsCommand):
    def handle_noargs(self, **options):

        BlogPost.objects.all().delete()

        for x in range(0,10):
            post = BlogPost(title=sentence())
            post.save()

            for x in range(0,3):
                v = BlogPostVersion(
                    blog = post,
                    copy = paragraphs(5,common=False),
                    published=datetime.datetime.now())
                v.save()
            #just make the last one added public
            v.public = True
            v.save()
