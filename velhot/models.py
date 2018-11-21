from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Discussions (models.Model):
    participants = []

class Group (models.Model):
    members = []
    posts = []

class Post(models.Model):
    post = models.CharField(max_length=2500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Publication Date', auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    real_name = models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone_number = models.CharField(validators=[phone_regex], max_length=17)

    def get_friendships(self):
  	    friendships = Friendship.objects.filter(creator=self.user)
  	    return friendships

class Friendship(models.Model):
    creator = models.ForeignKey(User, related_name="friendship_creator_set", on_delete=models.CASCADE)
    new_friend = models.ForeignKey(User, related_name="friend_set", on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    
    @classmethod
    def make_friend(cls, creator, new_friend, confirmed=True):
        friendship, created = cls.objects.get_or_create(
            creator = creator
        )
        friendship.users.add(new_friend)
