from gymApp import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('coach/', views.coach),
]
