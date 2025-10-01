from django.db import models
from auth_app.models import Account
from offers_app.models import OfferType

"""Choices for order status."""
class StatusType(models.TextChoices):
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'

"""Model for an order placed by a user."""
class Order(models.Model):   
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='orders')
    customer_user = models.PositiveIntegerField(blank=False, null=True)
    business_user = models.PositiveIntegerField(blank=False, null=True)
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField(default=0)
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=True)
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=10, choices=OfferType.choices, default=OfferType.STANDARD)
    status = models.CharField(max_length=12, choices=StatusType.choices, default=StatusType.IN_PROGRESS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Return the order title.
    def __str__(self):
        return self.title