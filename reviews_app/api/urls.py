from django.urls import path
from .views import ReviewsView, ReviewSingleView

""" URL patterns for review list and detail endpoints. """
urlpatterns = [
    path('reviews/', ReviewsView.as_view()),
    path('reviews/<int:id>/', ReviewSingleView.as_view(), name='review-detail')
]