from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperuserOrReadOnly(BasePermission):
    """
    Custom permission to allow superusers to perform any actions,
    and allow read-only access to authenticated users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in SAFE_METHODS:
                return True
            elif request.user.is_superuser:
                return True
        return False