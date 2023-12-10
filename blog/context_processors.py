"""blog/context_processors.py"""

from django.db.models import Count
from . import models


def base_context(requests):
    """Base context"""
    authors = models.Post.objects.published() \
        .get_authors() \
        .order_by('first_name')

    top_topics = models.Topic.objects \
        .annotate(post_counter_annotated1=Count('blog_posts')) \
        .order_by('-post_counter_annotated1')[:10]

    return {
        'authors': authors,
        'top_topics': top_topics,
    }
