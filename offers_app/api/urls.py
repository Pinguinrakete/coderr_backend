from django.urls import path
from .views import OffersView, OfferSingleView, OfferDetailView, ImageUploadView

""" URL patterns for offers, offer details, and image upload endpoints. """
urlpatterns = [
    path('offers/', OffersView.as_view()),
    path('offers/<int:id>/', OfferSingleView.as_view(), name='offer-specific'),
    path('offerdetails/<int:id>/', OfferDetailView.as_view(), name='offer-detail'),
    path('upload/', ImageUploadView.as_view(), name='image-upload')
]