""" blog/models.py"""

from django.conf import settings  # Imports Django's loaded settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class PostQuerySet(models.QuerySet):
    """Post Query Set"""
    def published(self):
        """published"""
        return self.filter(status=self.model.PUBLISHED)

    def draft(self):
        """Draft"""
        return self.filter(status=self.model.DRAFT)

    def get_authors(self):
        """get authors function"""
        user = get_user_model()
        return user.objects.filter(blog_posts__in=self).distinct()

    def get_topics(self):
        """get topics function"""
        return Topic.objects.all()


class Topic(models.Model):
    """Topic model"""
    name = models.CharField(
        max_length=50,
        unique=True  # To ensure no duplicates
    )

    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        """Meta"""
        ordering = ['name']

    objects = PostQuerySet.as_manager()

    def get_absolute_url(self):
        """Get absolute url function"""
        kwargs = {'slug': self.slug}
        return reverse('topic-detail', kwargs=kwargs)


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

    content = RichTextUploadingField()
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

    def get_absolute_url(self):
        """get absolute url function for posts"""
        if self.published:
            kwargs = {
                'year': self.published.year,
                'month': self.published.month,
                'day': self.published.day,
                'slug': self.slug
            }
        else:
            kwargs = {'pk': self.pk}

        return reverse('post-detail', kwargs=kwargs)

    class Meta:
        """Sort by the `created` field. the `-` prefix specifies
        to order in desc/reverse order.Otherwise, it will be in ascending order."""
        ordering = ['-created']

    def __str__(self):
        return self.title

    def publish(self):
        """publish function for posts"""
        self.status = self.PUBLISHED
        self.published = timezone.now()

    banner = models.ImageField(
        blank=True,
        null=True,
        help_text='A banner image for the post'
    )


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
        """meta"""
        ordering = ['-created']


class Contact(models.Model):
    """Contacts model"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        """meta"""
        ordering = ['-submitted']

    def __str__(self):
        return f'{self.submitted.date()}: {self.email}'


class PhotoContestSubmission(models.Model):
    """Photo contest model"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    photo_contest_entry = models.ImageField()
    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        """meta"""
        ordering = ['-submitted']

    def __str__(self):
        return f'{self.submitted.date()}: {self.email}'
