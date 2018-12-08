from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Channel (models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "channelmessages")
   
class Chat (models.Model):
    created = models.DateTimeField('Publication Date',auto_now_add=True)
    message = models.CharField(max_length=255,default = '')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, null=True, on_delete=models.CASCADE, related_name= "chatmessages")
    
    def __str__(self):
        return self.message, self.channel

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
    friends = models.ManyToManyField(User, blank=True, related_name="friends")

    @classmethod
    def remove_friend(cls, user, removable_friend):
        friend, created = cls.objects.get_or_create(
            user = user
        )
        friend.friends.remove(removable_friend)

class FriendRequest(models.Model):
	to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
	from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True) # set when created 

	def __str__(self):
		return "From {}, to {}".format(self.from_user.username, self.to_user.username)