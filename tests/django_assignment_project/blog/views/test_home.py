# tests/blog/views/test_home.py
from model_bakery import baker
from .views_model_bakery_custom_fields import rich_text_uploading_field
import pytest

from blog.models import Post

# Needed for database
pytestmark = pytest.mark.django_db


def custom_fields():
    return{
        'content': rich_text_uploading_field(),
    }


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200


def test_authors_included_in_context_data(client, django_user_model):
    """Checks that a list of unique published authors is included in the context and is ordered by first name"""

    # Make a published author called Cosmo
    cosmo = baker.make(
        django_user_model,
        username='ckramer',
        first_name='Cosmo',
        last_name='Kramer'
    )
    baker.make(
        'blog.Post',
        status=Post.PUBLISHED,
        author=cosmo,
        _quantity=2,
        **custom_fields(),
    )
    # Make a published author called Elaine
    elaine = baker.make(
        django_user_model,
        username='ebenez',
        first_name='Elaine',
        last_name='Benez'
    )
    baker.make(
        'blog.Post',
        status=Post.PUBLISHED,
        author=elaine,
        **custom_fields(),
    )

    # Make an unpublished author
    unpublished_author = baker.make(
        django_user_model,
        username='gcostanza'
    )

    baker.make('blog.Post', author=unpublished_author, status=Post.DRAFT, **custom_fields())

    # Expected Cosmo and Elaine to be returned, in this order
    expected = [cosmo, elaine]

    # Make a request to the home view
    response = client.get('/')

    # The context is available in the test response.
    result = response.context.get('authors')

    # Cast result (QuerrySet) to a list to compare
    assert list(result) == expected
