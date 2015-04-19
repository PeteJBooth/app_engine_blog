#CORE
import datetime
import random

#THIRD PARTY
from django.contrib.auth import get_user_model
from django.core import management
from django.core.management.base import NoArgsCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.webdesign.lorem_ipsum import paragraphs,sentence, words

#LOCAL
from blog.models import BlogPost, BlogPostVersion

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        user_cls = get_user_model()
        user = user_cls.objects.get(email='pete.j.booth@gmail.com')
        BlogPost.objects.all().delete()

        for x in range(0,10):
            count = random.randint(3,10)
            post = BlogPost(title=words(count,common=False), author=user)
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
