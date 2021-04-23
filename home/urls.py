from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name= "home"),
    path('about', views.about, name= "about"),
    path('contacts', views.contacts, name= "contacts"),
    path('signup', views.signupHandle, name= "signup"),
    path('login', views.loginHandle, name= "login"),
    path('logout', views.logoutHandle, name= "logout"),
    path('search', views.search, name= "search"),

]