from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from .models import Post, Schedule, Service
from django.utils.timezone import now
from .models import Trainer
import json


def trainer_detail(request, trainer_id):
    trainer = Trainer.objects.get(pk=trainer_id)
    return render(request, "trainer_detail.html", {"trainer": trainer})

def trainers_list(request):
    trainers = Trainer.objects.all()
    return render(request, "trainers.html", {"trainers": trainers})



def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

def coach(request):
    posts = Post.objects.all()
    return render(request, 'coach.html', {'posts': posts})

# def gym_schedule(request):
#     schedule = Schedule.objects.all().order_by("date_time")
#     return render(request, "gym_schedule.html", {"schedule":schedule})

def gym_schedule(request):
    schedule = Schedule.objects.all().order_by("date_time")

    time_slots = sorted(set(schedule.values_list("date_time__time", flat=True)))

    schedule_dict = {time: {day: None for day in range(1, 8)} for time in time_slots}

    for session in schedule:
        time = session.date_time.time()
        day_of_week = session.date_time.isoweekday() 
        schedule_dict[time][day_of_week] = session 

    return render(request, "gym_schedule.html", {"schedule_dict": schedule_dict})

def service_info(request, id):
    service = get_object_or_404(Service, id=id)
    schedule = Schedule.objects.filter(service=service) 
    return render(request, 'service_info.html', {'service': service, 'schedule': schedule})







