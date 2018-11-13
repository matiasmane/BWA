from django.db import models

class User (models.Model):
    real_name = models.CharField(max_length=255, unique=False)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True, default=None)
    phonenumber = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=255, unique=False)
    #test
