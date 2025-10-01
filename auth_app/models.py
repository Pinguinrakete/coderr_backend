from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

"""
Custom user model extending Django's AbstractUser. Adds a user_type field to distinguish between customer and business users.
Enforces user_type for regular users (not staff or superuser).
"""
class Account(AbstractUser):
    CUSTOMER = 'customer'
    BUSINESS = 'business'

    USER_TYPE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (BUSINESS, 'Business'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=True, blank=True)

    def clean(self):
        if not self.is_superuser and not self.is_staff and not self.user_type:
            raise ValidationError({'user_type': 'This field is required for regular users.'})
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)