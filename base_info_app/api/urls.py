from django.urls import path
from .views import BaseInfoView

"""
URL pattern for retrieving general platform statistics.

Endpoint:
- GET /base-info/  
  Returns platform-wide information including total reviews, average rating, number of business profiles, and total offers.

Permissions:
- Public (no authentication required)

Returns:
- review_count: Total number of reviews.
- average_rating: Average rating value.
- business_profile_count: Number of business user profiles.
- offer_count: Total number of posted offers.
"""
urlpatterns = [
    path('base-info/', BaseInfoView.as_view())
]