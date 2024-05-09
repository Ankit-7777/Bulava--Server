from django.urls import path
from WeddingApp.views import (
                            UserRegistrationView, UserLoginView,UserUpdateView,UserChangePasswordView,SendPasswordResetEmailView,
                            UserPasswordResetView,LogoutUserView,UserProfileView,AllUserProfileView,CategoryViewSet,EventViewSet

                            )

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)





urlpatterns = [
    

    
    path('user-registration/' ,UserRegistrationView.as_view(),name='register-UserProfile'),
    path('user-login',UserLoginView.as_view(),name='login-UserProfile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('user-update/<int:pk>/',UserUpdateView.as_view(),name='UserProfile-update'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('user-logout/', LogoutUserView.as_view(), name='user-logout'),
    path('users/', AllUserProfileView.as_view(), name='user_profile_list'),
    path('users/<int:pk>/', AllUserProfileView.as_view(), name='user_profile_detail'),
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('profile/', UserProfileView.as_view(), name='profile'), 
    path('categories/search/', CategoryViewSet.as_view({'get': 'search'}), name='category-search'),
    path('events/get-events-for-category/<int:category_id>/', EventViewSet.as_view({'get': 'get_events_for_category'}), name='event-get-events-for-category'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 




