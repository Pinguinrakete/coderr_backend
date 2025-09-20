from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max

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

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=CUSTOMER)
    customer_user = models.PositiveIntegerField(null=True, blank=True, unique=True)
    business_user = models.PositiveIntegerField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.user_type == self.CUSTOMER and self.customer_user is None:
                max_id = Account.objects.filter(user_type=self.CUSTOMER).aggregate(Max('customer_user'))['customer_user__max'] or 0
                self.customer_user = max_id + 1
            elif self.user_type == self.BUSINESS and self.business_user is None:
                max_id = Account.objects.filter(user_type=self.BUSINESS).aggregate(Max('business_user'))['business_user__max'] or 0
                self.business_user = max_id + 1
        super().save(*args, **kwargs)