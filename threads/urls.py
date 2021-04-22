from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.threads, name= "threads"),
    path('discussions', views.discussions, name= "discussions"),
    
   

]