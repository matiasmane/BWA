from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Post, Friend
from django.views import generic
from velhot.forms import SignUpForm, HomeForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def profile(request):
    return render(request, 'accounts/profile.html')

class Index(LoginRequiredMixin, generic.ListView):
    login_url = '/login'
    redirect_field_name = ''
    template_name = 'home/index.html'
    context_object_name = 'posts_list'
    
    def get(self, request):
        form = HomeForm()
        posts = Post.objects.all().order_by('-pub_date')
        users = User.objects.exclude(id=request.user.id)
        #friend = Friend.objects.get(current_user=request.user)
        #friends = friend.users.all()
      
        args = {
            'form': form, 'posts': posts, 'users': users, #'friends': friends
        }
        return render(request, self.template_name, args)

    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            post_text = form.save(commit=False)
            post_text.user = request.user
            post_text.save()
            text = form.cleaned_data['post']
            form = HomeForm()
            return redirect('/')

        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)

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

@login_required(login_url='/login')
def settings(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })

def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('/')