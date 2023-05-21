from django.contrib.auth.models import User
from django.db import models


class Comment(models.Model):
    creator =  models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.ManyToManyField('self', blank=True)
    likes = models.IntegerField(blank=True, null=True,  default=0)
    users_liked = models.ManyToManyField(User, related_name='comment_liked', blank=True)
    users_disliked = models.ManyToManyField(User, related_name='comment_disliked', blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def list_comments(self):
        return self.comments.all()[1:]

    def __str__(self) -> str:
        return self.content[0:50]


class Post(models.Model):
    title = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(blank=True, null=True,  default=0)
    users_liked = models.ManyToManyField(User, related_name='users_liked', blank=True)
    users_disliked = models.ManyToManyField(User, related_name='users_disliked', blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self) -> str:
        return self.title
    
