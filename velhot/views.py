from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Post, FriendRequest, Profile
from django.views import generic
from velhot.forms import SignUpForm, HomeForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

@login_required(login_url='/login')
def profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'accounts/profile.html', args)

class Index(LoginRequiredMixin, generic.ListView):
    login_url = '/login'
    redirect_field_name = ''
    template_name = 'home/index.html'
    context_object_name = 'posts_list'
    
    def get(self, request):
        form = HomeForm()
        posts = Post.objects.all().order_by('-pub_date')
        users = User.objects.exclude(id=request.user.id)
        p = Profile.objects.filter(user=request.user).first()
        friends = p.friends.all()
        sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
        rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)
        print(rec_friend_requests)

        args = {
            'form': form, 'posts': posts, 'users': users, 'friends': friends, 'sent_friend_requests': sent_friend_requests,
            'rec_friend_requests': rec_friend_requests }
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
            user = form.save()
            profile = Profile(address=form.cleaned_data.get('address'), phone_number=form.cleaned_data.get('phone_number'),
            real_name=form.cleaned_data.get('real_name'))
            profile.user = user
            profile.save()
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

@login_required(login_url='/login')
def discussions(request):
    return render(request, 'actions/discussions.html')


def send_friend_request(request, id):
	user = get_object_or_404(User, id=id)
	frequest, created = FriendRequest.objects.get_or_create(
		from_user=request.user,
		to_user=user)
	return redirect('/')

def accept_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.friends.add(user2)
    user2.profile.friends.add(user1)
    frequest.delete()
    return redirect('/')

def cancel_friend_request(request, id):
	user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(from_user=request.user, to_user=user).first()
	frequest.delete()
	return redirect('/')