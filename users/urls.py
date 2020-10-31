from django.contrib import admin
from django.urls import include, path

from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('captcha', include('captcha.urls')),
]