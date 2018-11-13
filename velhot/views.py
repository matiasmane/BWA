from django.shortcuts import render
from django.http import HttpResponse
from .models import User

def profile(user):
    return HttpResponse("Ripuli.")
