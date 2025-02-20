from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from .models import Post, Schedule
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

    # Отримуємо список унікальних годин початку занять
    time_slots = sorted(set(schedule.values_list("date_time__time", flat=True)))

    # Створюємо структуру даних для розкладу
    schedule_dict = {time: {day: "" for day in range(1, 8)} for time in time_slots}

    # Заповнюємо даними
    for session in schedule:
        time = session.date_time.time()
        day_of_week = session.date_time.isoweekday()  # 1 = Пн, 7 = Нд
        schedule_dict[time][day_of_week] = session.service.name  # Припускаю, що Service має поле name

    return render(request, "gym_schedule.html", {"schedule_dict": schedule_dict})

