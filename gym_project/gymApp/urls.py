from gymApp import views
from django.contrib import admin
from django.urls import path, include
from .views import trainers_list, trainer_detail
urlpatterns = [
    path('', views.index, name="index"),
    path('coach/', views.coach, name="coach"),
    path('gym_schedule/', views.gym_schedule, name="gym_schedule"),
    path("trainers/", trainers_list, name="trainers_list"),
    path("trainers/<int:trainer_id>/", trainer_detail, name="trainer_detail"),
]



