from django.db import models
from django.contrib.auth.models import User

class Discussion (models.Model):
    participants = []

class Group (models.Model):
    members = []
    posts = []

class Post(models.Model):
    post_text = models.CharField(max_length=2500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Publication Date')
    def __str__(self):
        return self.post_text

