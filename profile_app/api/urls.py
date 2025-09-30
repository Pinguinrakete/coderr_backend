from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ProfileSingleView, ProfilesBusinessView, ProfilesCustomerView

"""
URL patterns for Profile-related views.

Endpoints:
- GET, PATCH /profile/<pk>/ : Retrieve or update a specific user profile by user ID.
- GET /profiles/business/   : List all business user profiles.
- GET /profiles/customer/   : List all customer user profiles.
- PATCH /upload/            : Upload or update file for a user profile.

Additional:
- Serves media files in development mode when DEBUG=True.
"""
urlpatterns = [
    path('profile/<int:pk>/', ProfileSingleView.as_view(), name='profile-detail'),
    path('profiles/business/', ProfilesBusinessView.as_view()),
    path('profiles/customer/', ProfilesCustomerView.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)