from django.urls import path
from .views import ProfileSingleView, ProfilesBusinessView, ProfilesCustomerView

urlpatterns = [
    path('profile/<int:pk>/', ProfileSingleView.as_view(), name='profile-detail'),
    path('profiles/business/', ProfilesBusinessView.as_view()),
    path('profiles/customer/', ProfilesCustomerView.as_view())
]