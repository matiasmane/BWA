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
    