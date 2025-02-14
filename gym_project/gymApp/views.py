from django.shortcuts import render, get_object_or_404
from .models import Post, Schedule

def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

def coach(request):
    posts = Post.objects.all()
    return render(request, 'coach.html', {'posts': posts})

def gym_schedule(request):
    schedule = Schedule.objects.all()
    return render(request, "gym_schedule.html", {"schedule":schedule})

