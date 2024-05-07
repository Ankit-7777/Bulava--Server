from rest_framework.permissions import BasePermission

class IsSuperuser(BasePermission):
    """
    Custom permission to only allow superusers to view user details.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
