from django.urls import path
from .views import OffersView, OfferSingleView, OfferDetailsView, ImageUploadView

"""
URL patterns for offers management.

Endpoints:

- GET /offers/
  Retrieves a list of all offers.
  Returns: list of offers.

- GET /offers/<int:id>/
  Retrieves details of a specific offer identified by its ID.
  Returns: offer data or 404 if not found.

- GET /offerdetails/<int:id>/
  Retrieves detailed information for a specific offer identified by its ID.
  Returns: detailed offer data or 404 if not found.
"""
urlpatterns = [
    path('offers/', OffersView.as_view()),
    path('offers/<int:id>/', OfferSingleView.as_view(), name='offer-specific'),
    path('offerdetails/<int:id>/', OfferDetailsView.as_view(), name='offer-detail'),
    path('upload/', ImageUploadView.as_view(), name='image-upload')
]