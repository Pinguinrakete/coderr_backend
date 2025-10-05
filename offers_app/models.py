from django.db import models
from auth_app.models import Account

"""Choices for offer types."""
class OfferType(models.TextChoices):
    BASIC = 'basic', 'Basic'
    STANDARD = 'standard', 'Standard'
    PREMIUM = 'premium', 'Premium'

"""Model for details of an offer."""
class OfferDetail(models.Model):
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=True)
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=10, choices=OfferType.choices, default=OfferType.STANDARD)

    # Return the offer detail title.
    def __str__(self):
        return self.title
       
"""Model for an offer created by a business user."""
class Offer(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='offers', blank=False, editable=False)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offer_images/', blank=True, null=True)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    details = models.ManyToManyField(OfferDetail, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)