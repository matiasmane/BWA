from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Post
from django.views import generic
from velhot.forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

def profile(user):
    return HttpResponse("Ripuli.")

class Index(LoginRequiredMixin, generic.ListView):
    login_url = '/login'
    redirect_field_name = ''
    template_name = 'home/index.html'
    context_object_name = 'posts_list'
    
    def get_queryset(self):
        return Post.objects.order_by('-pub_date')

def post(request):
    return HttpResponse("This is a dummy view")

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

def settings(user):
    return HttpResponse("You can change your profile settings here.")
