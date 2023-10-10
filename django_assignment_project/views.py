"""django_assignment_project/views.py"""

from django.http import HttpResponse


def index(request):
    """index function to return content hello world to user"""
    return HttpResponse('Hello world!')
