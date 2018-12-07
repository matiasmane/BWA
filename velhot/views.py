from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Post, FriendRequest, Profile, Chat, Channel
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
from django.http import JsonResponse


@login_required(login_url='/login')
def profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    p = Profile.objects.filter(user=request.user).first()
    friends = p.friends.all()
    sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
    sent_to_users = set()
    for freaquest in sent_friend_requests:
        sent_to_users.add(freaquest.to_user)

    args = {'user': user, 'friends': friends, 'sent_friend_requests': sent_friend_requests,
            'sent_to_users': sent_to_users }
    
    return render(request, 'accounts/profile.html', args)

def own_chat(request):
    try:
        channel_creator = Channel.objects.get(creater=request.user)
        
    except:
        channel_creator = Channel(creater=request.user)
        
        channel_creator.save()
        print("hei", channel_creator.pk)
        print("hei", channel_creator.creater.id)
        print(request.user.pk)
        
       
    
    
    return redirect('/chat/'+ str(channel_creator.creater.id),request.user.pk,channel_creator.creater.id)
    

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
        rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)

        args = {
            'form': form, 'posts': posts, 'users': users, 'rec_friend_requests': rec_friend_requests }
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
def send_friend_request(request, id):
	user = get_object_or_404(User, id=id)
	frequest, created = FriendRequest.objects.get_or_create(
		from_user=request.user,
		to_user=user)
	return redirect('/profile/' + id)

#@login_required(login_url='/login')
#def create_own_channel(request,id):
#    from_user = get_object_or_404(User, id=id)
#    return redirect('actions/create_chat.html'+ id)

@login_required(login_url='/login')
def accept_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.friends.add(user2)
    user2.profile.friends.add(user1)
    frequest.delete()
    return redirect('/')


@login_required(login_url='/login')
def cancel_friend_request(request, id):
	user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(from_user=request.user, to_user=user).first()
	frequest.delete()
	return redirect('/')

@login_required(login_url='/login')
def remove_friendship(request, id):
    friend = get_object_or_404(User, id=id)
    Profile.remove_friend(request.user, friend)
    return redirect('/')

@login_required(login_url='/login')
def channel(request):
    return render(request, 'actions/create_chat.html')

@login_required(login_url='/login')
def chat(request, pk=None):
    if pk is None:
        
        Chat.objects.filter(channel=None)
        chat = Chat.objects.filter(channel=None)
        ctx = {
        'home': 'inactive',
        'chat': chat,
        }
        return render(request,'actions/chat.html',ctx)
    else:
        channel = Channel.objects.get(pk=pk)
    
    chats = Chat.objects.all()
    
    ctx = {
        'home': 'inactive',
        'chat': channelmessages,
        }
    return render(request, 'actions/chat.html', ctx)

@login_required(login_url='/login')
def chatpost(request,id=None):
    
    if id is None:
        if request.method == "POST":
            msg = request.POST.get('msgbox', None)
            print('Our value = ', msg)
            chat_message = Chat(user=request.user, message=msg)
            if msg != '':
                chat_message.save()
            return JsonResponse({'msg': msg, 'user': chat_message.user.username})
        else:
            return HttpResponse('Request must be POST.')

    else:
        if request.method == "POST":
            channel = get_object_or_404(Channel, id=id)
            msg = request.POST.get('msgbox', None)
            chat_message = Chat(user=request.user, message=msg, channel=channel)
            if msg != '':
                chat_message.save()
                return JsonResponse({'msg': msg, 'user': chat_message.user.username})
            else:
                return HttpResponse('Request must be POST')


@login_required(login_url='/login')
def chatmessages(request, id=None):
    if id is None:
        chat = Chat.objects.filter(channel__isnull=True)
    else:
        channel = get_object_or_404(Channel, id=id)
        chat = channel.chatmessages.all()
        print(channel)
    return render(request, 'actions/messages.html', {'chat': chat})

@login_required
def delete_own_comment(request, id):
    chat = get_object_or_404(Chat, pk=id)
    if chat.user == request.user:
        chat.delete()
    return JsonResponse({'success':'success'})
@login_required(login_url='/login')
def channelmessages(request):
    messages = Chat.objects.all()
    return render(request,'actions/chat.html', {'messages':messages})