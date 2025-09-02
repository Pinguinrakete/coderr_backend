from django.db import models
from auth_app.models import Account
from offers_app.models import OfferType

class StatusType(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

class Order(models.Model):   
    customer_user = models.PositiveIntegerField(null=True, blank=False)
    business_user = models.PositiveIntegerField(null=True, blank=False)
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=True)
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=10, choices=OfferType.choices, default=OfferType.STANDARD)
    status = models.CharField(max_length=12, choices=StatusType.choices, default=StatusType.IN_PROGRESS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title