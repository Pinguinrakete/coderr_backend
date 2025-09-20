from django.urls import path
from .views import RegistrationView, LoginView

"""
URL patterns for user authentication.

Endpoints:

- POST /registration/  
  Registers a new user.  
  Accepts: full name, email, password, repeated password and type (customer_user or business_user).  
  Returns: user data on success or validation errors.
  
- POST /login/
  Authenticates an existing user.
  Accepts: username and password.
  Returns: authentication token, username, email, user_id or error message on failure.
"""
urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login')
]