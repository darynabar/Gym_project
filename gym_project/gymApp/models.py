from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    def __str__(self):
        return self.username

class Trainer(models.Model):
   # user = models.ForeignKey(User, related_name='memberships', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    photo = models.CharField(max_length=2083)
    experience = models.IntegerField()
    
    SPECIALIZATION_CHOICES = [
        ("personal", "Персональний тренер"),
        ("group", "Тренер групових занять"),
    ]
    specialization = models.CharField(max_length=10, choices=SPECIALIZATION_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Service(models.Model):
    name = models.CharField(max_length=100)
    subscription = models.ForeignKey(Membership, on_delete=models.CASCADE) # зовн ключ до таблиці "Абонементи" - "Membership"
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.trainer})"
    
# зв'язок користувача з абонементами
class UserMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()  # закінчення абонемента

    def __str__(self):
        return f"{self.user} - {self.membership} (до {self.end_date})"

# зв'язок користувача з послугами
class UserService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="services")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)  # коли записався

    def __str__(self):
        return f"{self.user} - {self.service}"

# Абонементи
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

# Розклад занять
class Schedule(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    duration = models.DurationField()

    def __str__(self):
        return f"{self.service.name} з {self.trainer} ({self.date_time})"

# GymBar (додаткові товари або напої)
class GymBar(models.Model):
    CATEGORY_CHOICES = [
        ("protein", "Протеїновий коктейль"),
        ("snack", "Перекус"),
        ("drink", "Напій"),
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    volume = models.CharField(max_length=50, null=True, blank=True)  # Об'єм (наприклад, 500 мл)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

# Зали (Halls)
class Hall(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name
