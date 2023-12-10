# Generated by Django 4.2.5 on 2023-12-10 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_post_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoContestSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('photo_contest_entry', models.ImageField(blank=True, help_text='Submission for photo contest', null=True, upload_to='')),
                ('submitted', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-submitted'],
            },
        ),
    ]