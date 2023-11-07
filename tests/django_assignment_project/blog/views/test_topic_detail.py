# tests/blog/views/test_topic_detail.py

import pytest
from django.urls import reverse
from model_bakery import baker
from django.utils import timezone
from blog.models import Topic, Post
from time import sleep

# Needed for database
pytestmark = pytest.mark.django_db


def test_topic_get_absolute_url():
    """Test get_absolute_url on Topic model"""
    topic = baker.make(Topic, slug='this-is-my-test-topic')
    expected_url = reverse('topic-detail', kwargs={'slug': 'this-is-my-test-topic'})
    assert topic.get_absolute_url() == expected_url


def test_topic_detail_view(client, django_user_model):
    """Test detail view is reachable/only published posts visible/published posts appear in order of latest published"""
    topic = baker.make(Topic, name='test Topic1', slug='test-topic1')
    user = baker.make(django_user_model, username='test_user')

    test_post_1 = baker.make(
        Post,
        title='First Test post',
        slug='first-test-post',
        author=user,
        content='Test content1',
        status=Post.PUBLISHED,
        published=timezone.now(),
    )

    sleep(1)  # delay post creation to ensure published time is different

    test_post_2 = baker.make(
        Post,
        title='Second Test post',
        slug='second-test-post',
        author=user,
        content='Test content2',
        status=Post.PUBLISHED,
        published=timezone.now(),
    )

    test_post_3 = baker.make(
        Post,
        title='Third Test post',
        slug='Third-test-post',
        author=user,
        content='Test content3',
        status=Post.DRAFT,
        published=None,
    )

    test_post_1.topics.add(topic)
    test_post_2.topics.add(topic)
    test_post_3.topics.add(topic)

    url = reverse('topic-detail', kwargs={'slug': 'test-topic1'})

    response = client.get(url)

    assert response.status_code == 200

    content = response.content.decode('utf-8')
    pos_test_post_1 = content.find(test_post_1.title)
    pos_test_post_2 = content.find(test_post_2.title)
    pos_test_post_3 = content.find(test_post_3.title)
    assert pos_test_post_2 < pos_test_post_1  # Assert that Post 2 appears above Post 1 per publish order
    assert pos_test_post_3 == -1  # Assert that Post 3 doesn't appear in response content as it is not published
