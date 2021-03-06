from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    url(r'^chat/$', views.chat, name='chat'),
    url(r'^channel/$', views.channel, name='channel'),
    url(r'chatpost/$', views.chatpost, name='chatpost'),
    url(r'chatpost/(?P<id>\d+)/$', views.chatpost, name='chatpost'),
    url(r'^chatmessages/(?P<id>\d+)/$', views.chatmessages, name='chatmessages'),
    url(r'^chatmessages/$', views.chatmessages, name='chatmessages'),
    url(r'^profile/(?P<pk>\d+)/$', views.profile, name='view_profile_with_pk'),
    url(r'^chat/private_channel/$', views.own_chat, name='own_chat'),
    url(r'^chat/(?P<pk>\d+)/$', views.chat, name='view_chat_with_pk'),
    url(r'^friend-request/send/(?P<id>\d+)/$', views.send_friend_request, name='send_friend_request'),
    url(r'^friend-request/accept/(?P<id>\d+)/$', views.accept_friend_request, name='accept_friend_request'),
    url(r'^friend-request/cancel/(?P<id>\d+)/$', views.cancel_friend_request, name='cancel_friend_request'),
    url(r'^remove-friend/(?P<id>\d+)/$', views.remove_friendship, name='remove_friendship'),
    url(r'^message/(?P<id>\d+)/$', views.delete_own_comment, name='delete_chat'),
]