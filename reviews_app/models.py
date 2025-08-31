from django.db import models
from auth_app.models import Account

class Review(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_reviews')
    reviewer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='given_reviews')
    rating = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)