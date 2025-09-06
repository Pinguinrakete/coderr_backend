from django.db import models

class BaseInfo(models.Model):   
    review_count = models.PositiveIntegerField(default=0)
    average_rating = models.PositiveIntegerField(default=0)
    business_profile_count = models.PositiveIntegerField(default=0)
    offer_count = models.PositiveIntegerField(default=0)

