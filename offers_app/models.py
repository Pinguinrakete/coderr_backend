from django.db import models
from auth_app.models import Account

"""
Model definitions for service offers and their details.

OfferType:
- Enum for offer types: BASIC, STANDARD, PREMIUM.

OfferDetail:
- title (str): Name of the offer detail.
- revisions (int): Number of revisions allowed (default 0).
- delivery_time_in_days (int): Delivery time estimate.
- price (decimal): Price of this detail.
- features (JSON list): Optional list of features.
- offer_type (str): Type/category of the offer detail (default STANDARD).

Offer:
- user (FK): Owner account.
- title (str): Offer title.
- image (file): Optional image for the offer.
- description (str): Text description (optional).
- created_at, updated_at: Timestamps.
- details (M2M): Related OfferDetail instances.
- business_user (int): ID referencing business user (required).
"""
class OfferType(models.TextChoices):
        BASIC = 'basic', 'Basic'
        STANDARD = 'standard', 'Standard'
        PREMIUM = 'premium', 'Premium'

class OfferDetail(models.Model):
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=True)
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=10, choices=OfferType.choices, default=OfferType.STANDARD)

    def __str__(self):
        return self.title
       
class Offer(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offers/', blank=True, null=True)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    details = models.ManyToManyField(OfferDetail, blank=True)
    business_user = models.PositiveIntegerField(blank=False)