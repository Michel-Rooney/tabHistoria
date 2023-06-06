# Generated by Django 4.2.1 on 2023-06-06 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_rename_comment_disliked_comment_users_disliked_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='post',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='post',
            name='users_disliked',
        ),
        migrations.RemoveField(
            model_name='post',
            name='users_liked',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
