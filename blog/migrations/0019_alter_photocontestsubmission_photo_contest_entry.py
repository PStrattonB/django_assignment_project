# Generated by Django 4.2.5 on 2023-12-10 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_photocontestsubmission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photocontestsubmission',
            name='photo_contest_entry',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
