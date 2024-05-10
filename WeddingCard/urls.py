from django.contrib import admin
from django.urls import include, path
from WeddingApp import views
from rest_framework.routers import DefaultRouter
from WeddingApp.views import (
    CategoryViewSet,
    CoverImageViewSet,
    EventViewSet,
    ContectUsViewSet,
    UserRegistrationView,
    UserLoginView,
    UserUpdateView,
    UserChangePasswordView,
    SendPasswordResetEmailView,
    UserPasswordResetView,
    LogoutUserView,
    UserProfileView,
    AllUserProfileView,
)
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'cover-images', CoverImageViewSet, basename='coverimage')
router.register(r'events', EventViewSet, basename='events')
router.register(r'contect-us', ContectUsViewSet, basename='contect-us')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apis/', include('WeddingApp.urls')),
    path('auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('user-registration/', UserRegistrationView.as_view(), name='register-UserProfile'),
    path('user-login/', UserLoginView.as_view(), name='login-UserProfile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('user-update/<int:pk>/', UserUpdateView.as_view(), name='UserProfile-update'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('user-logout/', LogoutUserView.as_view(), name='user-logout'),
    path('users/', AllUserProfileView.as_view(), name='user_profile_list'),
    path('users/<int:pk>/', AllUserProfileView.as_view(), name='user_profile_detail'),
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('profile/', UserProfileView.as_view(), name='profile'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
