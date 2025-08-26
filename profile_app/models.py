from django.db import models
from auth_app.models import Account

class Profiles(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    description = models.TextField(default="")
    # file = models.FileField(upload_to='media/uploads/profiles/')
    # location = models.CharField(max_length=255, default="")
    # tel = models.CharField(max_length=20, default="")
    # working_hours = models.CharField(max_length=128, default="")
    # type = models.CharField(max_length=255, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description or f'Profile of {self.user.username}'

class FileUpload(models.Model):
    file = models.FileField(upload_to='media/uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)