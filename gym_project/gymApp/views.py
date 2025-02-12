from django.shortcuts import render
from .models import Post

def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

def coach(request):
    posts = Post.objects.all()
    return render(request, 'coach.html', {'posts': posts})

# Create your views here.
