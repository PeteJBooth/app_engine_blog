#THIRD PARTY
from django.contrib.auth import get_user_model
from django.views.generic import ArchiveIndexView, DetailView, FormView, YearArchiveView, MonthArchiveView, DayArchiveView
from google.appengine.api import users

#LOCAL
from .forms import BlogPostForm
from .models import BlogPost,BlogPostVersion


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


class BlogPostAddView(FormView):
    form_class = BlogPostForm
    success_url = '/' #can override this on submit
    template_name = 'blog/blogpostversion_add.html'

    def form_valid(self, form):
        user_cls = get_user_model()
        google_user = users.get_current_user()

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
