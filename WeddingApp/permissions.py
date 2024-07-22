from rest_framework.permissions import BasePermission, SAFE_METHODS
from WeddingApp.models import Event
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import PermissionDenied

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
        try:
            if request.user and request.user.is_authenticated:
                if request.method in SAFE_METHODS:
                    return True
            return False
        except ObjectDoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        try:
            if request.user and request.user.is_authenticated:
                if request.method in SAFE_METHODS:
                    if not obj.is_private:
                        return True
                    elif obj.user == request.user or obj.invited.filter(id=request.user.id).exists():
                        return True
                if obj.user == request.user:
                    return True
            return False
        except ObjectDoesNotExist:
            return False
