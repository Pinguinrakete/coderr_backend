from django.urls import path
from .views import OffersView, OfferSingleView, OfferDetailsView

urlpatterns = [
    path('offers/', OffersView.as_view()),
    path('offers/<int:id>/', OfferSingleView.as_view(), name='offer-specific'),
    path('offerdetails/<int:id>/', OfferDetailsView.as_view(), name='offer-detail')
]