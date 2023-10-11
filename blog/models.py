from django.conf import settings  # Imports Django's loaded settings
from django.db import models
from django.utils import timezone


class Topic(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True  # To ensure no duplicates
    )

    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=self.model.PUBLISHED)

    def draft(self):
        return self.filter(status=self.model.DRAFT)


class Post(models.Model):
    """Represents a blog post"""
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]

    title = models.CharField(
        max_length=255,
        null=False
    )

    slug = models.SlugField(
        null=False,
        help_text='This is a slug field',
        unique_for_date='published',  # Slug is unique for publication date
    )

    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # The Django auth user model
        on_delete=models.PROTECT,  # Prevent posts from being deleted
        related_name='blog_posts',  # "This" on the user model
        null=False
    )

    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)  # Sets on creation
    updated = models.DateTimeField(auto_now=True)  # Updates on each save

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make this post publicly visible',
        null=False,
    )

    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date & time this article was published',
    )

    objects = PostQuerySet.as_manager()

    class Meta:
        # Sort by the `created` field. the `-` prefix specifies to order in desc/reverse order. Otherwise, it will be
        # in ascending order.
        ordering = ['-created']

    def __str__(self):
        return self.title

    def publish(self):
        self.status = self.PUBLISHED
        self.published = timezone.now()


class Comment(models.Model):
    """Represents a comment made by a user"""

    post = models.OneToOneField(
        Post,
        related_name='comments',
        on_delete=models.CASCADE,
        null=False,
    )

    name = models.CharField(
        max_length=255,
        null=False,
    )

    email = models.EmailField(
        max_length=255,
        null=False
    )

    text = models.TextField(
        max_length=500,
        null=False
    )

    approved = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)  # Sets on creation
    updated = models.DateTimeField(auto_now=True)  # Updates on each save

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-created']
