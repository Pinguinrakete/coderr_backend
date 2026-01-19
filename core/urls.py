from django.contrib import admin
from django.urls import path, include

""" API URL patterns for all application modules. """
api_urlpatterns = [
    path('', include('auth_app.api.urls')),
    path('', include('profile_app.api.urls')),
    path('', include('offers_app.api.urls')),
    path('', include('orders_app.api.urls')),
    path('', include('reviews_app.api.urls')),
    path('', include('base_info_app.api.urls')),
]

""" Main URL patterns for admin, authentication, and API endpoints. """
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(api_urlpatterns)),
]
