# tests/blog/views/test_topic_list.py

import pytest
from django.urls import reverse

# Needed for database
pytestmark = pytest.mark.django_db


def test_topic_list_view(client):
    """Test that we can reach topic-list template"""
    response = client.get(reverse('topic-list'))
    assert response.status_code == 200
