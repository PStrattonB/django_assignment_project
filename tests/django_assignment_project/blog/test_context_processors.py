# tests/blog/views/test_home.py

import pytest
from blog.context_processors import base_context

pytestmark = pytest.mark.django_db


def test_base_context_top_topics():
    """Test to confirm top topics is accessible from base_context function"""
    context = base_context(None)
    print(context)
    assert 'top_topics' in context

