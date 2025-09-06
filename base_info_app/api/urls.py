from django.urls import path
from .views import BaseInfoView

"""
URL pattern for retrieving base information.

Endpoint:

- GET /base-info/
  Retrieves general base information.
  Returns: base information data.
"""
urlpatterns = [
    path('base-info/', BaseInfoView.as_view())
]