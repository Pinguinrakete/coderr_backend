from django.db import models
from auth_app.models import Account
from offers_app.models import OfferType

"""
Model for customer orders based on offers.

StatusType:
- Enum for order status: IN_PROGRESS, COMPLETED, CANCELLED.

Order:
- user (FK): Account who placed the order.
- customer_user (int): ID of the customer user.
- business_user (int): ID of the business user providing the offer.
- title (str): Title of the order.
- revisions (int): Number of allowed revisions (default 0).
- delivery_time_in_days (int): Estimated delivery time.
- price (decimal): Order price.
- features (JSON list): Optional list of order features.
- offer_type (str): Type/category of the offer.
- status (str): Current order status (default IN_PROGRESS).
- created_at, updated_at: Timestamps.
"""
class StatusType(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

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

    def __str__(self):
        return self.title