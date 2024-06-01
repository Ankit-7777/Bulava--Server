from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from django.http import JsonResponse, Http404
from django.contrib.auth import views as auth_views, logout as django_logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.views import LoginView as AuthLoginView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from WeddingApp.renderers import UserProfileRenderer
from rest_framework.decorators import action
from rest_framework import status
from WeddingApp.utils import Utils
from WeddingApp.mytokens import get_tokens_for_user
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from WeddingApp.models import UserProfile, Category, CoverImage, Event, ContactUs
from WeddingApp.permissions import IsSuperuserOrReadOnly
from django.core.mail import send_mail
from WeddingApp.serializers import (
    UserProfileSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserUpdateSerializer,
    UserChangePasswordSerializer,
    SendPasswordResetEmailSerializer,
    UserPasswordResetSerializer,
)

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.db.models.functions import Lower
from django.db.models import Q
from WeddingApp.pagination import MyPageNumberPagination
from WeddingApp.renderers import UserProfileRenderer




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
            response = Response({'token':token,'user_detail':serializer.data}, status=status.HTTP_200_OK)
            return response
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

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
                response = Response({'token':token,'user_detail':serializer.data}, status=status.HTTP_200_OK)
                return response
                
            else:
                return Response({'error':{'non_field_errors':['Email or Password is Not Valid']},},status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status.HTTP_422_UNPROCESSABLE_ENTITY)

class LogoutUserView(APIView):
    renderer_classes = [UserProfileRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        django_logout(request)  # Clear the session
        response = Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
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
                'user_detail': updated_data
            })
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class UserChangePasswordView(APIView):
    renderer_classes=[UserProfileRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self, request, formate=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
     
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserProfileRenderer]
    def post(self, request, format =None):
        serializer = SendPasswordResetEmailSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({ 'message':'Password Reset link send. Please check your Email'}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_422_UNPROCESSABLE_ENTITY)
         
class UserPasswordResetView(APIView):
    renderer_classes =[UserProfileRenderer]
    def post(self, request,uid, token, format =None):
        serializer = UserPasswordResetSerializer(data=request.data,context={'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception = True):
            return Response({'message':'Password Reset Successfully'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
