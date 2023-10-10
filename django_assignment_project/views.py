# django_assignment_project/views.py

from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello world!')
