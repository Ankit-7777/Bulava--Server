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
from WeddingApp.models import UserProfile,Category, CoverImage, BirthdayParty, Wedding, InaugurationEvent
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
        BirthdayPartySerializer,
        WeddingSerializer,
        InaugurationEventSerializer,
)

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models.functions import Lower
from django.db.models import Q
from WeddingApp.pagination import MyPageNumberPagination





class AllUserProfileView(APIView):
    renderer_classes = [UserProfileRenderer]
    permission_classes = [IsSuperuser]
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

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = [UserProfileRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperuser]
    pagination_class = MyPageNumberPagination

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
    permission_classes = [IsSuperuser]
    pagination_class = MyPageNumberPagination

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

class BirthdayPartyViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserProfileRenderer]
    permission_classes = [IsSuperuser]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = BirthdayParty.objects.all()
    serializer_class = BirthdayPartySerializer
    
    
    def retrieve(self, request, pk=None):
        try:
            birthday_party = self.get_queryset().get(id=pk)
            serializer = BirthdayPartySerializer(birthday_party)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BirthdayParty.DoesNotExist:
            return Response({"message": "Birthday party not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Birthday party created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            instance = self.get_queryset().get(id=pk)
            serializer = BirthdayPartySerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Birthday party updated successfully", "data": serializer.data})
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except BirthdayParty.DoesNotExist:
            return Response({"message": "Birthday party not found"}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            instance = self.get_queryset().get(id=pk)
            serializer = BirthdayPartySerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Birthday party partially updated successfully", "data": serializer.data})
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except BirthdayParty.DoesNotExist:
            return Response({"message": "Birthday party not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            instance = self.get_queryset().get(id=pk)
            instance.delete()
            return Response({"message": "Birthday party deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except BirthdayParty.DoesNotExist:
            return Response({"message": "Birthday party not found"}, status=status.HTTP_404_NOT_FOUND)

class WeddingEventViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserProfileRenderer]
    permission_classes = [IsSuperuser]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Wedding.objects.all()
    serializer_class = WeddingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Wedding event created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk):
        try:
            wedding = self.get_queryset().get(id=pk)
            serializer = WeddingSerializer(wedding)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Wedding.DoesNotExist:
            return Response({"message": "Wedding event not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        try:
            instance = self.get_queryset().get(id=pk)
            serializer = self.get_serializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Wedding event updated successfully", "data": serializer.data})
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Wedding.DoesNotExist:
            return Response({"message": "Wedding event not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def partial_update(self, request, pk=None):
        try:
            instance = self.get_queryset().get(id=pk)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Wedding event partially updated successfully", "data": serializer.data})
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Wedding.DoesNotExist:
            return Response({"message": "Wedding event not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        try:
            instance = self.get_queryset().get(id=pk)
            instance.delete()
            return Response({"message": "Wedding event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Wedding.DoesNotExist:
            return Response({"message": "Wedding event not found"}, status=status.HTTP_404_NOT_FOUND)

class InaugurationEventViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserProfileRenderer]
    permission_classes = [IsSuperuser]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = InaugurationEvent.objects.all()
    serializer_class = InaugurationEventSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Inauguration event created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk):
        try:
            inauguration_event = self.get_queryset().get(id=pk)
            serializer = InaugurationEventSerializer(inauguration_event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except InaugurationEvent.DoesNotExist:
            return Response({"message": "Inauguration event not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        try:
            instance = self.get_queryset().get(id=pk)
            serializer = self.get_serializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Inauguration event updated successfully", "data": serializer.data})
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except InaugurationEvent.DoesNotExist:
            return Response({"message": "Inauguration event not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def partial_update(self, request, pk=None):
        try:
            instance = self.get_queryset().get(id=pk)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Inauguration event partially updated successfully", "data": serializer.data})
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except InaugurationEvent.DoesNotExist:
            return Response({"message": "Inauguration event not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        try:
            instance = self.get_queryset().get(id=pk)
            instance.delete()
            return Response({"message": "Inauguration event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except InaugurationEvent.DoesNotExist:
            return Response({"message": "Inauguration event not found"}, status=status.HTTP_404_NOT_FOUND)
