# Generated by Django 4.2.1 on 2023-05-19 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_comment_comment_disliked_comment_comment_liked_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment',
        ),
        migrations.AddField(
            model_name='comment',
            name='comments',
            field=models.ManyToManyField(blank=True, to='client.comment'),
        ),
    ]