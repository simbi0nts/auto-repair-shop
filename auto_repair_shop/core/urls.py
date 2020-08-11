
from django.contrib.auth import views as auth_views
from django.urls import path
import core.views.profile as profile
import core.views.homepage as homepage


urlpatterns = [
    path('', homepage.home, name='home'),
    path('profile/', profile.profile, name='profile'),
    path('register/', profile.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
]
