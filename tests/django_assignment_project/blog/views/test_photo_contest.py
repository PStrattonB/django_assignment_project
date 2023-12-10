# tests/blog/views/test_photo_contest.py

import pytest
from django.urls import reverse
from blog.models import PhotoContestSubmission
from PIL import Image

# Needed for database
pytestmark = pytest.mark.django_db


def test_photo_contest_get(client):
    response = client.get(reverse('photo-contest-form'))
    assert response.status_code == 200


def test_photo_contest_valid_post(client, tmpdir):
    temp_image = tmpdir.join("dummy_pic.jpg")

    image = Image.new("RGB", (100, 100), "white")
    image.save(str(temp_image), format="JPEG")

    with open(str(temp_image), 'rb') as image_file:
        contest_user_data = {
            'first_name': 'Stratton',
            'last_name': 'Barry',
            'email': 'Test@test.com',
            'photo_contest_entry': image_file
        }

        response = client.post(
            reverse('photo-contest-form'),
            data=contest_user_data,
            follow=True
        )

        # Test that the post request succeeded
        assert response.status_code == 200
        # Test that we landed on the home page and the success message displayed
        assert b'Thank you! Your photo contest submission has been received. Good luck!' in response.content
        # Test that the submission is present in the database
        assert PhotoContestSubmission.objects.filter(first_name='Stratton', last_name='Barry').exists()
