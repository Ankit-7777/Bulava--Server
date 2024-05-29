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
from WeddingApp.models import UserProfile,Category, CoverImage,Event,ContactUs
from WeddingApp.permissions import IsSuperuserOrReadOnly
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
        EventSerializer,
        ContactUsSerializer,
       
)

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models.functions import Lower
from django.db.models import Q
from WeddingApp.pagination import MyPageNumberPagination



class AllUserProfileView(APIView):
    renderer_classes = [UserProfileRenderer]
    permission_classes = [IsSuperuserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    
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
    authentication_classes = [JWTAuthentication]
    
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

    def get_object(self):
        user = self.request.user # Accessing the user associated with the token
        if not user:
            raise NotFound("User not found")
        return user

    def put(self, request, format=None):
        user = self.get_object()

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            updated_data = serializer.data  # Retrieve updated data
            return Response({
                'message': 'User profile updated successfully',
                'data': updated_data
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

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = [UserProfileRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperuserOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "Category created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Category updated successfully", "data": serializer.data})

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Category partially updated successfully", "data": serializer.data})

    def destroy(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

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
            return Response({"message": "Cover image created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
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

class EventViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserProfileRenderer]
    permission_classes = [IsSuperuserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    def create(self, request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Event created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error":  serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request,pk):
        try:
            event = self.get_queryset().get(id=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({"message": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def partial_update(self, request, pk=None):
        try:
            instance = self.get_queryset().get(id=pk)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Event partially updated successfully", "data": serializer.data})
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Event.DoesNotExist:
            return Response({"message": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self,request,pk=None):
        try:
            instance = self.get_queryset().get(id=pk)
            instance.delete()
            return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            return Response({"message": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
    
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
            return JsonResponse({"message": "Events retrieved successfully", "data": serializer.data}, status=200)
        else:
            return JsonResponse({"message": "No events found for the provided category"}, status=404)

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
            return Response({"message": "Message sent successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error":  serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
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
            return Response({"message": "Message deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ContactUs.DoesNotExist:
            return Response({"message": "Message not found"}, status=status.HTTP_404_NOT_FOUND)
