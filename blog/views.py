#THIRD PARTY
from django.views.generic import ArchiveIndexView, DetailView, FormView, YearArchiveView, MonthArchiveView, DayArchiveView

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
    form = BlogPostForm
