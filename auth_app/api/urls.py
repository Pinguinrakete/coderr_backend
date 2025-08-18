from django.urls import path
from .views import RegistrationView

"""
URL patterns for user authentication.

Endpoints:

- POST /registration/  
  Registers a new user.  
  Accepts: full name, email, password, repeated password.  
  Returns: user data on success or validation errors.
"""
urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    # path('login/', LoginView.as_view(), name='login')
]