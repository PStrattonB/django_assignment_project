# blog/views.py

from django.shortcuts import render
from . import models
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
# Create your views here.


class HomeView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        # get parent context
        context = super().get_context_data(**kwargs)

        latest_posts = models.Post.objects.published() \
            .order_by('-published')[:3]

        # update the context with our context variables
        context.update({
            'latest_posts': latest_posts
        })

        return context


class AboutView(TemplateView):
    template_name = 'blog/about.html'


def terms_and_conditions(request):
    return render(request, 'blog/terms_and_conditions.html')


class PostListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')  # Customized queryset


class TopicListView(ListView):
    model = models.Topic
    context_object_name = 'topics'
    queryset = models.Topic.objects.order_by('name')


class PostDetailView(DetailView):
    model = models.Post

    def get_queryset(self):
        # Get base queryset
        queryset = super().get_queryset().published()

        # if this is a 'pk' lookup, use default queryset
        if 'pk' in self.kwargs:
            return queryset

        # otherwise, filter on the published date
        return queryset.filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )


class TopicDetailView(DetailView):
    model = models.Topic

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = self.get_object()

        posts = topic.blog_posts.filter(status='published').order_by('-published')

        context.update({
            'posts': posts
        })
        return context
