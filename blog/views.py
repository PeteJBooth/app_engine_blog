#THIRD PARTY
from djangae.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import ArchiveIndexView, DetailView, FormView, YearArchiveView, MonthArchiveView, DayArchiveView
from google.appengine.api import users


#LOCAL
from .forms import BlogPostForm
from .models import BlogPost,BlogPostVersion

class AdminOnlyMixin(object):
    """
    Overrides the dispatch method of any implementing views to ensure only
    Admin users have access.
    """
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(AdminOnlyMixin, self).dispatch(*args, **kwargs)


class BlogPostIndexView(ArchiveIndexView):
    allow_empty = True
    #because the datastore can't do joins I'm going to use the version model
    #to pull back the posts
    model = BlogPostVersion
    date_field = 'published'


class BlogPostYearView(YearArchiveView):
    allow_empty = True
    model = BlogPostVersion
    date_field = 'published'


class BlogPostMonthView(MonthArchiveView):
    allow_empty = True
    model = BlogPostVersion
    month_format = '%m'
    date_field = 'published'


class BlogPostDayView(DayArchiveView):
    allow_empty = True
    model = BlogPostVersion
    month_format = '%m'
    date_field = 'published'


class BlogPostDetailView(DetailView):
    model = BlogPost
    context_object_name = 'post'

    def post(self, request, *args, **kwargs):
        #TODO: make this secure (and less hacky)
        version = BlogPostVersion.objects.get(id=self.request.POST['version_id'])
        version.blog.versions.update(public=False)
        version.public = True
        version.save()

        return HttpResponseRedirect(reverse('post_detail',kwargs={'slug':version.blog.slug }))


class BlogPostAddView(AdminOnlyMixin, FormView):
    form_class = BlogPostForm
    success_url = '/' #can override this on submit
    template_name = 'blog/blogpostversion_add.html'

    def form_valid(self, form):
        user_cls = get_user_model()
        google_user = users.get_current_user()

        #need to the associated Django object from the datastore 
        #based on the unique id of the authenticated google user.
        #TODO: Check if this breaks if a different auth model is used
        user = user_cls.objects.get(username=google_user.user_id())

        post = BlogPost(
            title=form.cleaned_data['title'],
            slug=form.cleaned_data['slug'],
            author=user
            )
        post.save()
        version = BlogPostVersion(
            blog = post,
            copy = form.cleaned_data['copy'],
            published = form.cleaned_data['published'],)
        version.save()

        return super(BlogPostAddView,self).form_valid(form)
