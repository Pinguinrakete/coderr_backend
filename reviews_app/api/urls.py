from django.urls import path
from .views import ReviewsView, ReviewSingleView

urlpatterns = [
    path('reviews/', ReviewsView.as_view()),
    path('reviews/<int:id>/', ReviewSingleView.as_view(), name='review-detail')
]