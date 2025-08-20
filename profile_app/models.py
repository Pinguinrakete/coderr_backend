from django.db import models
from django.conf import settings

class Offers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='offers')
    file = models.FileField(upload_to='media/uploads/offers/', blank=True, null=True)
    location = models.CharField(max_length=255)
    tel = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=128, blank=True) 
    type = models.CharField(max_length=255, blank=True) 
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.type} @ {self.location}"
    

class FileUpload(models.Model):
    file = models.FileField(upload_to='media/uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)