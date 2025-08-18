from django.contrib.auth.models import AbstractUser
from django.db import models

"""
Model representing a user account.

Fields:
- username (CharField): Inherited from AbstractUser. The unique username of the account.
- email (EmailField): Inherited from AbstractUser. The user's email address.
- password (CharField): Inherited from AbstractUser. The hashed user password.
- user_type (CharField): Specifies the type of user.
    Choices:
        - "customer": Regular customer account.
        - "business": Business account.
    Default: "customer".

Methods:
- __str__(): Returns the username as the string representation of the account.
"""
class Account(AbstractUser):
    CUSTOMER = 'customer'
    BUSINESS = 'business'

    USER_TYPE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (BUSINESS, 'Business'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=CUSTOMER)