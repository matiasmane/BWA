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
    path('discussions/', views.discussions, name='discussions'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.add_friend, name='add_friend')
    
]