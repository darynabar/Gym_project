from gymApp import views
from django.contrib import admin
from django.urls import path, include
from .views import service_info, trainers_list, trainer_detail,membership_list, page_contact
urlpatterns = [
    path('', views.index, name="index"),
    path('coach/', views.coach, name="coach"),
    path('gym_schedule/', views.gym_schedule, name="gym_schedule"),
    path("trainers/", trainers_list, name="trainers_list"),
    path("trainers/<int:trainer_id>/", trainer_detail, name="trainer_detail"),

    path("membership/", views.membership_list, name="membership_list"), 
    path("membership_list/", views.membership_list, name="membership_list"),
    path('service/<int:id>/', service_info, name='service_info'),
    path('contacts/', page_contact, name='contacts')
    path('search/', views.search, name='search'),

]



