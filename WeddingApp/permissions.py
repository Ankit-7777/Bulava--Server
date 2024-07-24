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
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method == 'POST':
            return True

        if request.method in SAFE_METHODS:
            return self._can_view_event_list_or_detail(request)

        if request.method in ['PATCH', 'PUT', 'DELETE']:
            event = self._get_event_from_request(request)
            return self._can_modify_event(request, view, event)    
        return False

    def _can_view_event_list_or_detail(self, request):
        event = self._get_event_from_request(request)
        if request.method == 'GET':
            if event is None:
                return True
            return self._can_view_event(request, event)
        return False

    def _can_view_event(self, request, event):
        if event is None:
            return False
        if not event.is_private:
            return True
        return event.user == request.user or event.invited.filter(id=request.user.id).exists()

    def _can_modify_event(self, request, view, event):
        if event is None:
            return False
        return event.user == request.user

    def _get_event_from_request(self, request):
        event_id = self._get_event_id_from_request(request)
        if event_id:
            return self._get_event_by_id(event_id)
        return None

    def _get_event_id_from_request(self, request):
        return request.parser_context['kwargs'].get('pk', None)

    def _get_event_by_id(self, event_id):
        try:
            return Event.objects.get(id=event_id)
        except ObjectDoesNotExist:
            return None
