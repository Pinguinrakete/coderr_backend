from django.urls import path
from .views import RegistrationView, LoginView

""" URL patterns for user registration and login endpoints. """
urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login')
]