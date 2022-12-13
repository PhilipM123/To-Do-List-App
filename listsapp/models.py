from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class ListItem(models.Model):
    content = models.CharField(max_length=30)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ('-timestamp',)

    def serialize(self):
        return {
            "completed" : self.completed,
        }

class List(models.Model):
    title = models.CharField(max_length=30, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="user")
    listitems = models.ManyToManyField(ListItem, blank=True, related_name="listitem")
    timestamp = models.DateTimeField()
    userwatchlist = models.ManyToManyField("User", related_name="watchlist")
    public = models.BooleanField(default=True, blank=True)

    class Meta:
        ordering = ('-timestamp',)

class Follow(models.Model):
    # The user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='follower')
    # the lists they are following
    following = models.ForeignKey(List, on_delete=models.CASCADE, null=True, related_name='following')

    class Meta:
        unique_together = ('user', 'following')

class Category(models.Model):
    title = models.CharField(max_length=30)
    lists = models.ForeignKey(List, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('title',)