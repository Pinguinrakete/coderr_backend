from rest_framework.permissions import BasePermission
from auth_app.models import Account

""" Allows access only to authenticated users with user_type = 'business'. """
class IsBusinessUser(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and getattr(request.user, 'user_type', None) == Account.BUSINESS
        )