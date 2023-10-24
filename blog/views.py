# blog/views.py

from django.shortcuts import render
from . import models
from django.db.models import Count
# Create your views here.


def home(request):
    """The Blog Homepage"""

    # Get last 3 posts
    latest_posts = models.Post.objects.published().order_by('-published')[:3]
    # Get authors
    authors = models.Post.objects.published().get_authors().order_by('first_name')
    # Get top 10 topics ordered by use in posts
    top_topics = models.Topic.objects.annotate(post_counter_annotated1=Count('blog_posts')).order_by('-post_counter_annotated1')[:10]
    # Add as context variable "latest_posts"
    context = {
        'top_topics': top_topics,
        'authors': authors,
        'latest_posts': latest_posts
    }
    return render(request, 'blog/home.html', context)
