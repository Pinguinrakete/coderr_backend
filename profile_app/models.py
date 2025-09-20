from django.db import models
from auth_app.models import Account

"""
Model representing a user's profile.

Fields:
- user (OneToOneField): Links to Account model, primary key.
- description (TextField): Optional user description.
- file (FileField): Optional file upload related to the profile.
- uploaded_at (DateTimeField): Timestamp of last file upload.
- location (CharField): Optional location information.
- tel (CharField): Optional telephone number.
- working_hours (CharField): Optional working hours description.

String representation:
- Returns description if present, otherwise 'Profile of <username>'.
"""
class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    description = models.TextField(blank=True, default="")
    file = models.FileField(upload_to='profiles/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255, blank=True, default="")
    tel = models.CharField(max_length=20, blank=True, default="")
    working_hours = models.CharField(max_length=128, blank=True, default="")

    def __str__(self):
        return self.description or f'Profile of {self.user.username}'