from django.db import models


class Follower(models.Model):
    follower_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.follower_name


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User')
    age = models.IntegerField(null=True)
    followers = models.ManyToManyField(Follower)


class Blog(models.Model):
    title = models.CharField(max_length=20)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User')
