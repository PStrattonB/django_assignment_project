# tests/blog/models/model_bakery_custom_fields.py

from model_bakery.recipe import seq


def rich_text_uploading_field():
    return seq("Default text for RichTextUploadingField")
