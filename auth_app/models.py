from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max
from django.core.exceptions import ValidationError

"""
Model representing a user account.

Inherits from:
- AbstractUser: Provides default Django user fields like username, email, and password.

Fields:
- username (CharField): Inherited from AbstractUser. The unique username of the account.
- email (EmailField): Inherited from AbstractUser. The user's email address.
- password (CharField): Inherited from AbstractUser. The hashed user password.
- user_type (CharField): Specifies the type of user.
    Choices:
        - "customer": Regular customer account.
        - "business": Business account.
    Default: "customer".
- customer_user (PositiveIntegerField): Unique incremental ID for customer accounts. Auto-assigned on creation.
- business_user (PositiveIntegerField): Unique incremental ID for business accounts. Auto-assigned on creation.

Methods:
- save(*args, **kwargs): Overrides the default save method to assign a sequential ID
  to either customer_user or business_user depending on the user_type, if not already set.
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