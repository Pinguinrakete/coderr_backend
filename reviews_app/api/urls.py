from django.urls import path
from .views import ReviewsView, ReviewSingleView

"""
URL patterns for reviews management.

Endpoints:

- GET /reviews/
  Retrieves a list of all reviews.
  Returns: list of reviews.

- POST /reviews/
  Creates a new review.
  Returns: created review data.

- PATCH /reviews/<int:id>/
  Partially updates a specific review identified by its ID.
  Returns: updated review data or 404 if not found.

- DELETE /reviews/<int:id>/
  Deletes a specific review identified by its ID.
  Returns: 204 No Content or 404 if not found.
"""
urlpatterns = [
    path('reviews/', ReviewsView.as_view()),
    path('reviews/<int:id>/', ReviewSingleView.as_view(), name='review-detail')
]