from django.urls import path
from .views import OffersView, OfferSingleView, OfferDetailsView, ImageUploadView

"""
URL Patterns for Offer-related API endpoints.

Endpoints:

GET, POST /offers/
- Handled by OffersView
- List all offers or create a new offer.

GET, PATCH, DELETE /offers/<int:id>/
- Handled by OfferSingleView
- Retrieve, partially update, or delete a specific offer by ID.
- URL name: 'offer-specific'

GET /offerdetails/<int:id>/
- Handled by OfferDetailsView
- Retrieve details of a specific offer detail by ID.
- URL name: 'offer-detail'

PATCH /upload/
- Handled by ImageUploadView
- Upload or update an image for an existing offer.
- URL name: 'image-upload'
"""
urlpatterns = [
    path('offers/', OffersView.as_view()),
    path('offers/<int:id>/', OfferSingleView.as_view(), name='offer-specific'),
    path('offerdetails/<int:id>/', OfferDetailsView.as_view(), name='offer-detail'),
    path('upload/', ImageUploadView.as_view(), name='image-upload')
]