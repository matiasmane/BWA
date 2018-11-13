from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Post
from django.views import generic

def profile(user):
    return HttpResponse("Ripuli.")

def login(user):
    return HttpResponse("Login")

class Index(generic.ListView):
    
    template_name = 'home/index.html'
    context_object_name = 'posts_list'
    
    def get_queryset(self):
        return Post.objects.order_by('-pub_date')

def post(request):
    return HttpResponse("This is a dummy view")