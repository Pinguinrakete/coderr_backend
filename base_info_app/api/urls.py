from django.urls import path
from .views import BaseInfoView

""" URL pattern for retrieving base platform statistics. """
urlpatterns = [
    path('base-info/', BaseInfoView.as_view())
]