from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ProfileSingleView, ProfilesBusinessView, ProfilesCustomerView

""" URL patterns for profile detail and profile lists. """
urlpatterns = [
    path('profile/<int:pk>/', ProfileSingleView.as_view(), name='profile-detail'),
    path('profiles/business/', ProfilesBusinessView.as_view()),
    path('profiles/customer/', ProfilesCustomerView.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)