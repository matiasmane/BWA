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
    path('chat/', views.chat, name='chat'),
    url(r'post/$', views.chatpost, name='post'),
    url(r'^profile/(?P<pk>\d+)/$', views.profile, name='view_profile_with_pk'),
    url(r'^friend-request/send/(?P<id>\d+)/$', views.send_friend_request, name='send_friend_request'),
    url(r'^friend-request/accept/(?P<id>\d+)/$', views.accept_friend_request, name='accept_friend_request'),
    url(r'^friend-request/cancel/(?P<id>\d+)/$', views.cancel_friend_request, name='cancel_friend_request'),
    url(r'^remove-friend/(?P<id>\d+)/$', views.remove_friendship, name='remove_friendship'),

]