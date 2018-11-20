from django.db import models
from django.contrib.auth.models import User

class Discussion (models.Model):
    participants = []

class Group (models.Model):
    members = []
    posts = []

class Post(models.Model):
    post = models.CharField(max_length=2500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Publication Date', auto_now_add=True)

class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)    