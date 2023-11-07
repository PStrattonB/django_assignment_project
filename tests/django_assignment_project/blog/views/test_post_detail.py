# tests/blog/views/test_post_detail.py
from model_bakery import baker
import pytest
from django.utils import timezone
from blog.models import Post, Topic
from django.urls import reverse

# Needed for database
pytestmark = pytest.mark.django_db


def test_topic_links_on_post_detail(client, django_user_model):
    """Testing that topic links on post detail view work as expected"""
    topic = Topic.objects.create(name='Test Topic', slug='test-topic')
    user = baker.make(django_user_model, username='test_user')

    post = baker.make(
        Post,
        title='Test Post',
        slug='test-post',
        author=user,
        content='Test content',
        status='published',
        published=timezone.now(),
    )

    post.topics.add(topic)

    response = client.get(
        reverse(
            'post-detail',
            kwargs={
                'year': post.published.year,
                'month': post.published.month,
                'day': post.published.day,
                'slug': 'test-post'}))

    assert response.status_code == 200
    assert topic.name.encode() in response.content
    assert topic.get_absolute_url().encode() in response.content

