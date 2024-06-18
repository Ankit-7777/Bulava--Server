from rest_framework.permissions import BasePermission, SAFE_METHODS
from WeddingApp.models import Event

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

class IsEventOwner(BasePermission):
    """
    Custom permission to only allow owners of an event to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user

