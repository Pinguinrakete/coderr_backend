from django.db import models
from auth_app.models import Account

class Rewiew(models.Model):
    business_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received-reviews')
    reviewer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='given-reviews')
    rating = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['business_user', 'reviewer'], name='unique-review-per-business_user')]