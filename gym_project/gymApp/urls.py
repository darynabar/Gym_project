from gymApp import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.index),
    path('coach/', views.coach),
]
