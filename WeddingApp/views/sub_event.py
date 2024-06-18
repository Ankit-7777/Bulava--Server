from django.http import JsonResponse
from rest_framework.response import Response
from WeddingApp.renderers import UserProfileRenderer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from WeddingApp.permissions import IsSuperuserOrReadOnly
from WeddingApp.serializers import SubEventSerializer
from WeddingApp.pagination import MyPageNumberPagination
from WeddingApp.models import Category, SubEvent, Event
from rest_framework.permissions import IsAuthenticated

class SubEventViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserProfileRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = SubEvent.objects.all()
    serializer_class = SubEventSerializer
    pagination_class = MyPageNumberPagination
    
    def get_queryset(self):
        if not self.request.user.is_superuser:
            return SubEvent.objects.filter(user=self.request.user)
        return super().get_queryset()
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(
                {"message": "Sub event updated successfully", "sub_event_detail": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def partial_update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(
                {"message": "Sub event partially updated successfully", "sub_event_detail": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def destroy(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Sub event deleted successfully"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def get_subevent_for_events(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return JsonResponse({"error": "Event not found"}, status=404)
        
        sub_events = SubEvent.objects.filter(event_id=event_id)
        serializer = self.get_serializer(sub_events, many=True)
        if not sub_events.exists():
            return Response({"message": "No sub events found for the provided event"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Sub events found successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    
    # New method for getting subevents by category
    @action(detail=False, methods=['get'])
    def get_subevents_for_category(self, request, category_id):
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return JsonResponse({"error": "Category not found"}, status=404)

        sub_events = SubEvent.objects.filter(category=category_id)
        serializer = self.get_serializer(sub_events, many=True)
        if not sub_events.exists():
            return Response({"message": "No sub events found for the provided Category"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Sub events found successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def sub_event_name_search(self, request):
        search_str = request.query_params.get('search_str')
        if not search_str:
            return Response({"message": "Search query cannot be empty"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        queryset = SubEvent.objects.all()
        search_str = search_str.lower()
        queryset = queryset.filter(name__icontains=search_str)
        serializer = self.get_serializer(queryset, many=True)
        if not queryset.exists():
            return Response({"message": "No sub events found for the provided search query"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Sub events found successfully", "data": serializer.data}, status=status.HTTP_200_OK)