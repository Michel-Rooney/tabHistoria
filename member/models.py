from django.contrib.auth.models import User
from django.db import models


class Comment(models.Model):
    creator =  models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ManyToManyField('self')
    likes = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self) -> str:
        return self.creator


class Post(models.Model):
    title = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(blank=True, null=True)
    comments = models.ManyToManyField(Comment)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self) -> str:
        return self.title
    
