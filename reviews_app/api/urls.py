from django.urls import path
from .views import ReviewsView, ReviewSingleView

"""
URL patterns for reviews management.

Endpoints:

- GET /reviews/
  Retrieves a list of all reviews.
  Returns: list of reviews.

- GET /reviews/<int:id>/
  Retrieves details of a specific review identified by its ID.
  Returns: review data or 404 if not found.
"""
urlpatterns = [
    path('reviews/', ReviewsView.as_view()),
    path('reviews/<int:id>/', ReviewSingleView.as_view(), name='review-detail')
]