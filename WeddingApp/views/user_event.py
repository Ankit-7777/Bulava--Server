from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from WeddingApp.models import UserEvent
from WeddingApp.serializers import UserEventSerializer
from WeddingApp.renderers import UserProfileRenderer
from rest_framework.decorators import action

class UserEventViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserProfileRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserEvent.objects.all()
    serializer_class = UserEventSerializer
    
    def get_queryset(self):
        queryset = UserEvent.objects.filter(guest=self.request.user)
        event_status = self.request.query_params.get('status')
        if event_status in ['accepted', 'ignored', 'declined']:
            queryset = queryset.filter(status=event_status)
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='change-status')
    def change_status(self, request, pk=None):
        event = self.get_object()
        status_value = request.data.get('status')
        valid_status_choices = [choice[0] for choice in UserEvent.STATUS_CHOICES]
        if status_value not in valid_status_choices:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        event.status = status_value
        event.save()
        serializer = self.get_serializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
