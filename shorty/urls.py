
from shorty.views import delete
from django.urls import path, re_path
from django.contrib.auth import views as auth_view
from . import views as user_view



urlpatterns = [
        path('', user_view.index, name="index"),
        path('login', auth_view.LoginView.as_view(template_name="shorty/login.html"), name="login"),
        path('logout', auth_view.LogoutView.as_view(template_name = "shorty/index.html"), name="logout"),
        path('signup', user_view.signup, name="signup"),
        path('home', user_view.home, name="home"),
        path('delete/<slug:slug>', user_view.delete, name="delete"),
        path('<slug:slug>', user_view.slug_redirect, name="slug_redirect")
        ]
