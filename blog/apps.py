"""blog/Apps.py"""
from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Blog config"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
