from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ProfileSingleView, ProfilesBusinessView, ProfilesCustomerView, FileUploadView

"""
URL patterns for user profiles management.

Endpoints:

- GET /profile/<int:pk>/
  Retrieves the profile of a user identified by primary key (pk).
  Returns: user profile data or 404 if not found.

- GET /profiles/business/
  Retrieves a list of all business user profiles.
  Returns: list of business profiles.

- GET /profiles/customer/
  Retrieves a list of all customer user profiles.
  Returns: list of customer profiles.
"""
urlpatterns = [
    path('profile/<int:pk>/', ProfileSingleView.as_view(), name='profile-detail'),
    path('profiles/business/', ProfilesBusinessView.as_view()),
    path('profiles/customer/', ProfilesCustomerView.as_view()),
    path('upload/', FileUploadView.as_view(), name='file-upload')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)