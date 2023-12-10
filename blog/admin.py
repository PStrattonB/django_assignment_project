"""blog/admin.py"""
from django.contrib import admin
from . import models


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin comment module"""

    list_display = (
        'post',
        'name',
        'email',
        'approved',
        'created',
        'updated',
    )

    search_fields = (
        'name',
        'email',
        'approved',
    )

    list_filter = (
        'approved',
    )


class InLineComment(admin.StackedInline):
    """In line comments"""
    model = models.Comment

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ['name', 'text', 'email']
        return readonly_fields


@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    """Admin topic module"""
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    """Admin post module"""
    list_display = (
        'title',
        'author',
        'status',
        'created',
        'updated',
    )

    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )

    list_filter = (
        'status',
        'topics',
    )

    prepopulated_fields = {'slug': ('title',)}

    inlines = [InLineComment]

# admin.site.register(models.Post, PostAdmin)


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin contact module"""
    list_display = (
        'email',
        'last_name',
        'first_name',
        'submitted',
    )
    # Make these fields read-only in the admin
    readonly_fields = (
        'first_name',
        'last_name',
        'email',
        'message',
        'submitted',
    )


@admin.register(models.PhotoContestSubmission)
class PhotoContestAdmin(admin.ModelAdmin):
    """Admin photo contest module"""
    list_display = (
        'email',
        'last_name',
        'first_name',
        'submitted',
    )

    readonly_fields = (
        'first_name',
        'last_name',
        'email',
        'photo_contest_entry',
        'submitted',
    )
