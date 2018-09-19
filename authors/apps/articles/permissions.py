"""This module contains custom permissions"""
from rest_framework import permissions


class IsSuperuser(permissions.BasePermission):
    """
    Check if it is a super user.
    """

    def has_permission(self, request, view):
        """Check if a user trying to access the end point is a super user"""
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
            return True
        return False
