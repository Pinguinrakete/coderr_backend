from django.db import models
from auth_app.models import Account
from django.core.validators import MinValueValidator, MaxValueValidator

"""Model for user reviews of business users."""
class Review(models.Model):
    business_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='business_user_review', blank=False, null=False)
    reviewer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='given_reviews')
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)