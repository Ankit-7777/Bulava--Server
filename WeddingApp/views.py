from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth import views as auth_views
from django.contrib.auth.hashers import check_password
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth import logout as django_logout 
from rest_framework.views import APIView
from WeddingApp.renderers import UserProfileRenderer
from django.utils.decorators import method_decorator 
from rest_framework import status 
from WeddingApp.utils import Utils
from WeddingApp.mytokens import get_tokens_for_user
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from WeddingApp.models import UserProfile,Category, CoverImage
from WeddingApp.permissions import IsSuperuser
from django.core.mail import send_mail
from django.http import Http404
from WeddingApp.serializers import (
        UserProfileSerializer,
        UserRegistrationSerializer,
        UserLoginSerializer,
        UserUpdateSerializer,
        UserChangePasswordSerializer,
        SendPasswordResetEmailSerializer,
        UserPasswordResetSerializer,
        CategorySerializer,
        CoverImageSerializer,
)

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models.functions import Lower
from django.db.models import Q
from WeddingApp.pagination import MyPageNumberPagination



#UserProfile Apis

class AllUserProfileView(APIView):
    renderer_classes = [UserProfileRenderer]
    permission_classes = [IsSuperuser]
    
    def get(self, request, pk=None):
        if pk is not None:
            return self.get_single_user(pk)
        else:
            return self.get_all_users()

    def get_single_user(self, pk):
        try:
            user = UserProfile.objects.get(id=pk)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get_all_users(self):
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    renderer_classes = [UserProfileRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, formate=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status = status.HTTP_200_OK)

class UserRegistrationView(APIView):
    renderer_classes=[UserProfileRenderer]
    
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            response = Response({'token':token,'msg': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes=[UserProfileRenderer]
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=UserProfile.objects.get(email=email)
            
            if user is not None and check_password(password,user.password):
                
                serializer=UserProfileSerializer(user)
                token=get_tokens_for_user(user)
                response = Response({'token':token,'msg':'Success','messages':f'You Have Successfully {email} Logined Into Your Account','user_detail':serializer.data}, status=status.HTTP_200_OK)
                return response
                
            else:
                return Response({'message':'Check if your','error':{'non_field_errors':['Email or Password is Not Valid']},'msg':'Error'},status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,{'msg':'Error'},status.HTTP_400_BAD_REQUEST)

class LogoutUserView(APIView):
    renderer_classes = [UserProfileRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        django_logout(request)  # Clear the session
        response = Response({'msg': 'Logged out successfully'}, status=status.HTTP_200_OK)
        response.delete_cookie('token')  # Delete the token cookie
        return response

class UserUpdateView(APIView):
    renderer_classes=[UserProfileRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get_object(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User profile updated successfully',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserChangePasswordView(APIView):
    renderer_classes=[UserProfileRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, formate=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserProfileRenderer]
    def post(self, request, format =None):
        serializer = SendPasswordResetEmailSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({ 'msg':'Password Reset link send. Please check your Email'}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
         
class UserPasswordResetView(APIView):
    renderer_classes =[UserProfileRenderer]
    def post(self, request,uid, token, format =None):
        serializer = UserPasswordResetSerializer(data=request.data,context={'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception = True):
            return Response({'msg':'Password Reset Successfully'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Category Apis
class CategoryViewSet(viewsets.ViewSet):
    renderer_classes = [UserProfileRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperuser]
    pagination_class = MyPageNumberPagination

    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Category created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        try:
            category = Category.objects.get(id=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        try:
            category = Category.objects.get(id=pk)
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Category updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        try:
            category = Category.objects.get(id=pk)
            category.delete()
            return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['GET'], name='category_name_search')
    def search(self, request):
        search_str = request.query_params.get('search_str')
        if not search_str:
            return Response({"message": "Search query cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = Category.objects.all()
        search_str = search_str.lower()
        queryset = queryset.filter(category_name__icontains=search_str)
        
        if not queryset.exists():
            return Response({"message": "No categories found for the provided search query"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(queryset, many=True)
        return Response({"message": "Categories found successfully", "data": serializer.data}, status=status.HTTP_200_OK)

#Cover Image Apis
class CoverImageViewSet(viewsets.ViewSet):
    renderer_classes = [UserProfileRenderer]
    permission_classes = [IsSuperuser]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination

    def list(self, request):
        """
        Retrieve a list of all CoverImage instances.
        """
        cover_images = CoverImage.objects.all()
        serializer = CoverImageSerializer(cover_images, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CoverImageSerializer(data=request.data)
        
        # Check if the image already exists
        if 'image' in request.data:
            existing_images = CoverImage.objects.filter(image=request.data['image'])
            if existing_images.exists():
                return Response({"error": "Image already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cover image created successfully"}, status=status.HTTP_201_CREATED)
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
                return Response({"message": "Cover image updated successfully"}, status=status.HTTP_200_OK)
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
