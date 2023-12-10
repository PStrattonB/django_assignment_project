"""tests/django_assignment_project/blog/models/test_post.py"""

from model_bakery import baker
import pytest
from blog.models import Post
import datetime as dt
from freezegun import freeze_time
from .model_bakery_custom_fields import rich_text_uploading_field


# Mark this test Module as requiring the database
pytestmark = pytest.mark.django_db


def custom_fields():
    return{
        'content': rich_text_uploading_field(),
    }


def test_published_posts_only_returns_those_with_published_status():
    # Create a published Post by setting the status to "published"
    published = baker.make('blog.Post', status=Post.PUBLISHED, **custom_fields())
    # Create a draft Post
    baker.make('blog.Post', status=Post.DRAFT, **custom_fields())

    # We expect only the "published" object to be returned
    expected = [published]
    # Cast the result as a list, so we can compare apples with apples
    # Lists and querysets are of different types
    result = list(Post.objects.published())

    assert result == expected


def test_draft_posts_only_returns_those_with_draft_status():
    draft = baker.make('blog.Post', status=Post.DRAFT, **custom_fields())
    baker.make('blog.Post', status=Post.PUBLISHED, **custom_fields())

    expected = [draft]
    result = list(Post.objects.draft())

    assert result == expected


def test_publish_sets_status_to_published():
    post = baker.make('blog.Post', status=Post.DRAFT, **custom_fields())
    post.publish()
    assert post.status == Post.PUBLISHED


@freeze_time(dt.datetime(2030, 6, 1, 12), tz_offset=0)  # Replaces now()
def test_publish_sets_published_to_current_datetime():
    # Create a new post, and ensure no published datetime is set
    post = baker.make('blog.Post', published=None, **custom_fields())
    post.publish()

    # Set the timezone to UTC (to match tz_offset=0)
    assert post.published == dt.datetime(2030, 6, 1, 12, tzinfo=dt.timezone.utc)


def test_get_authors_returns_users_who_have_authored_a_post(django_user_model):
    # Create a user
    author = baker.make(django_user_model)
    # Create a post that is authored by the user
    baker.make('blog.Post', author=author, **custom_fields())
    # Create another user - but this one won't have any posts
    baker.make(django_user_model)

    assert list(Post.objects.get_authors()) == [author]


def test_get_authors_returns_unique_users(django_user_model):
    # Create a user
    author = baker.make(django_user_model)
    # Create multiple posts. The _quantity argument can be used to specify how many objs to create
    baker.make('blog.Post', author=author, _quantity=3, **custom_fields())

    assert list(Post.objects.get_authors()) == [author]
