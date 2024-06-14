from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from rest_framework.decorators import action
from WeddingApp.models import CoverImage, Category
from WeddingApp.permissions import IsSuperuserOrReadOnly
from WeddingApp.serializers import CoverImageSerializer
from WeddingApp.pagination import MyPageNumberPagination
from WeddingApp.renderers import UserProfileRenderer


class CoverImageViewSet(viewsets.ModelViewSet):
    queryset = CoverImage.objects.all()
    serializer_class = CoverImageSerializer
    renderer_classes = [UserProfileRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperuserOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        try:
            cover_image = CoverImage.objects.get(id=pk)
            serializer = CoverImageSerializer(cover_image)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CoverImage.DoesNotExist:
            return Response({"message": "Cover image not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            cover_image = CoverImage.objects.get(id=pk)
            serializer = CoverImageSerializer(cover_image, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Cover image updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CoverImage.DoesNotExist:
            return Response({"message": "Cover image not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def partial_update(self, request, pk=None):
        try:
            cover_image = CoverImage.objects.get(id=pk)
            serializer = CoverImageSerializer(cover_image, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Cover image partially updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CoverImage.DoesNotExist:
            return Response({"message": "Cover image not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            cover_image = CoverImage.objects.get(id=pk)
            cover_image.delete()
            return Response({"message": "Cover image deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except CoverImage.DoesNotExist:
            return Response({"message": "Cover image not found"}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=False, methods=['get'], url_path='get-cover-image-for-category')
    def get_cover_images_for_category_type(self, request, category_type):
        try:
            category = Category.objects.get(id=category_type)
            cover_images = CoverImage.objects.filter(event_category=category)
            serializer = CoverImageSerializer(cover_images, many=True)
            if not cover_images.exists():
                return Response({"message": "No cover images found for the provided category"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Cover images found successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
