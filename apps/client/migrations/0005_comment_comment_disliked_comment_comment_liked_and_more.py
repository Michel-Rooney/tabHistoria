# Generated by Django 4.2.1 on 2023-05-19 17:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0004_post_users_disliked_post_users_liked_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_disliked',
            field=models.ManyToManyField(blank=True, related_name='comment_disliked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_liked',
            field=models.ManyToManyField(blank=True, related_name='comment_liked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='likes',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
