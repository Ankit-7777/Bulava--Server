from rest_framework.permissions import BasePermission, SAFE_METHODS
from WeddingApp.models import Event
from django.core.exceptions import ObjectDoesNotExist

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

class EventPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if not obj.is_private:
                return True
            if request.user and request.user.is_authenticated:
                return obj.user == request.user or obj.invited.filter(id=request.user.id).exists()
            return False
        return obj.user == request.user

