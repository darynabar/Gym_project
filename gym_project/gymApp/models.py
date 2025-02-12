from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta




class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#  Користувач
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.username

class Membership(models.Model):
    name = models.CharField(max_length=100)
    DURATION_CHOICES = [
        ("monthly", "Місячний"),
        ("yearly", "Річний"),
        ("one-time", "Разовий"),
    ]
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.get_duration_display()})"

class Trainer(models.Model):
   # user = models.ForeignKey(User, related_name='memberships', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    photo = models.CharField(max_length=2083)
    experience = models.CharField(max_length=2083)
    
    SPECIALIZATION_CHOICES = [
        ("personal", "Персональний тренер"),
        ("group", "Тренер групових занять"),
    ]
    specialization = models.CharField(max_length=10, choices=SPECIALIZATION_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Service(models.Model):
    name = models.CharField(max_length=100)
    subscription = models.ForeignKey(Membership, on_delete=models.CASCADE) 
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.trainer})"
    

class UserService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="services")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.user} - {self.service}"



class Schedule(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    duration = models.DurationField()

    def __str__(self):
        return f"{self.service.name} з {self.trainer} ({self.date_time})"

class GymBar(models.Model):
    CATEGORY_CHOICES = [
        ("protein", "Протеїновий коктейль"),
        ("snack", "Перекус"),
        ("drink", "Напій"),
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    volume = models.CharField(max_length=50, null=True, blank=True)  

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

# class Hall(models.Model):
#     name = models.CharField(max_length=100)
#     capacity = models.IntegerField()

#     def __str__(self):
#         return self.name
    
class UserMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField() 

    def save(self, *args, **kwargs):
        if not self.end_date:
            if self.membership.duration == "monthly":
                self.end_date = self.start_date + timedelta(days=30)
            elif self.membership.duration == "yearly":
                self.end_date = self.start_date + timedelta(days=365)
            elif self.membership.duration == "one-time":
                self.end_date = self.start_date 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.membership} (до {self.end_date})"

class UserSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE) 
    is_attending = models.BooleanField(default=True) 
