from django.db import models
from auth_app.models import Account
from django.core.validators import MinValueValidator, MaxValueValidator

"""
Model representing a review left by a customer for a business user.

Fields:
- business_user (int): ID of the reviewed business user (not a FK for flexibility).
- reviewer (FK to Account): The user who wrote the review.
- rating (int): Star rating between 1 and 5.
- description (str): Optional review text.
- created_at (datetime): Timestamp of creation.
- updated_at (datetime): Timestamp of last update.
"""
class Review(models.Model):
    business_user = models.IntegerField()
    reviewer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='given_reviews')
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)