from gymApp import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.index, name="index"),
    path('coach/', views.coach, name="coach"),
    path('gym_schedule/', views.gym_schedule, name="gym_schedule"),
]
