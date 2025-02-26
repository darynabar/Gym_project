from datetime import timedelta
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.views import LogoutView
from gymApp.forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import Post, Schedule, Service,Membership, UserMembership, UserSchedule, UserService
from django.utils.timezone import now
from .models import Trainer
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def page_contact(request):
    return render(request, 'contacts.html') 


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

def membership_list(request):
    memberships = Membership.objects.order_by('-price') 
    return render(request, 'membership_list.html', {'memberships': memberships})


def search(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return redirect("home")  

    trainers = Trainer.objects.filter(first_name__icontains=query) | Trainer.objects.filter(last_name__icontains=query)
    
    services = Service.objects.filter(name__icontains=query)

    if Membership.objects.filter(name__icontains=query).exists():
        return redirect("subscriptions")  

    return render(request, "search_results.html", {"query": query, "trainers": trainers, "services": services})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class CustomLogoutView(LogoutView):
    next_page = '/' 

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Ви успішно вийшли із системи.")
        return super().dispatch(request, *args, **kwargs)

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/') 
            else:
                messages.error(request, 'Невірні дані для входу')
        else:
            messages.error(request, 'Будь ласка, перевірте введені дані')

    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


@login_required
def user_profile(request):
    user = request.user
    memberships = UserMembership.objects.filter(user=user).first()
    services = UserService.objects.filter(user=user)
    user_schedule = UserSchedule.objects.filter(user=user).prefetch_related('schedule')
    schedule_dict = {}

    for user_sched in user_schedule:
        schedule = user_sched.schedule
        time_slot = schedule.date_time.strftime("%H:%M")
        day_of_week = schedule.date_time.isoweekday() - 1  

        if time_slot not in schedule_dict:
            schedule_dict[time_slot] = { 
                0: None,  
                1: None,  
                2: None,  
                3: None,  
                4: None,  
                5: None,  
                6: None   
            }
        if day_of_week in schedule_dict[time_slot]:
            schedule_dict[time_slot][day_of_week] = schedule

    print("User Schedule Dict:", schedule_dict)

    context = {
        "user": user,
        "memberships": memberships,
        "services": services,
        "schedule_dict": schedule_dict,
    }
    return render(request, "user_profile.html", context)
