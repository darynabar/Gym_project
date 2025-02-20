from gymApp import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("gymApp.urls")),
    path("trainers/", views.trainers_list, name="trainers"),
    path('trainers/<int:trainer_id>/', views.trainer_detail, name='trainer_detail'),
]
