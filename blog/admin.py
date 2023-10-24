"""blog/admin.py"""
from django.contrib import admin
from . import models


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
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
    model = models.Comment

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ['name', 'text', 'email']
        return readonly_fields


@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
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
