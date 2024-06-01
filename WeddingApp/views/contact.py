from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from WeddingApp.models import ContactUs
from WeddingApp.serializers import ContactUsSerializer
from WeddingApp.pagination import MyPageNumberPagination
from WeddingApp.renderers import UserProfileRenderer


class ContectUsViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserProfileRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = MyPageNumberPagination
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    
    def create(self, request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Message sent successfully", "contact_detail": serializer.data}, status=status.HTTP_200_OK)
        return Response({"error":  serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    def retrieve(self, request,pk):
        try:
            contact_us = self.get_queryset().get(id=pk)
            serializer = ContactUsSerializer(contact_us)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ContactUs.DoesNotExist:
            return Response({"message": "Message not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self,request,pk=None):
        try:
            instance = self.get_queryset().get(id=pk)
            instance.delete()
            return Response({"message": "Message deleted successfully"}, status=status.HTTP_200_OK)
        except ContactUs.DoesNotExist:
            return Response({"message": "Message not found"}, status=status.HTTP_404_NOT_FOUND)
