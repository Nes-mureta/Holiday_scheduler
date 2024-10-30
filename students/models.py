from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    level_of_education = models.CharField(max_length=100)  # You can use a choice field for predefined levels
    school_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Timetable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    day = models.CharField(max_length=20)
    time_slot = models.CharField(max_length=20,null=True)  # e.g., '08:00 AM - 09:00 AM'

    def __str__(self):
        return f"{self.subject} on {self.day} at {self.time_slot}"