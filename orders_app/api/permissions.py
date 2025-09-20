from rest_framework.permissions import BasePermission

"""
Custom permission class to allow access only to staff users.

Methods:
- has_permission: Returns True if the requesting user exists and is marked as staff.
"""
class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff