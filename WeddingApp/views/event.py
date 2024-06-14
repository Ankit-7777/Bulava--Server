from django.http import JsonResponse
from rest_framework.response import Response
from WeddingApp.renderers import UserProfileRenderer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from WeddingApp.models import Event
from WeddingApp.permissions import IsSuperuserOrReadOnly
from WeddingApp.serializers import EventSerializer
from WeddingApp.pagination import MyPageNumberPagination
from WeddingApp.models import Category
from rest_framework.permissions import IsAuthenticated


class EventViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserProfileRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    def create(self, request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error":  serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def retrieve(self, request,pk):
        try:
            event = self.get_queryset().get(id=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({"Event": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def partial_update(self, request, pk=None):
        try:
            instance = self.get_queryset().get(id=pk)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Event partially updated successfully", "event_detail":serializer.data})
            return Response({"errors": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Event.DoesNotExist:
            return Response({"Event": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self,request,pk=None):
        try:
            instance = self.get_queryset().get(id=pk)
            instance.delete()
            return Response({"message": "Event deleted successfully"}, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({"Event": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # New method for getting events by category
    @action(detail=False, methods=['get'], url_path='get-events-for-category')
    def get_events_for_category(self, request, category_id):
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return JsonResponse({"error": "Category not found"}, status=404)

        events = Event.objects.filter(event_category_id=category_id)
        serializer = EventSerializer(events, many=True)

        if events.exists():
            return JsonResponse({"message": "Events retrieved successfully", "event_detail": serializer.data}, status=200)
        else:
            return JsonResponse({"message": "No events found for the provided category"}, status=404)
