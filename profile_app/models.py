from django.db import models
from auth_app.models import Account

class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    description = models.TextField(blank=True, default="")
    file = models.FileField(upload_to='uploads/profiles/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, default="")
    tel = models.CharField(max_length=20, blank=True, default="")
    working_hours = models.CharField(max_length=128, blank=True, default="")

    def __str__(self):
        return self.description or f'Profile of {self.user.username}'