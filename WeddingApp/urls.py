from django.urls import path
from WeddingApp.views import (
                            UserRegistrationView, UserLoginView,UserUpdateView,UserChangePasswordView,SendPasswordResetEmailView,
                            UserPasswordResetView,LogoutUserView,UserProfileView,
                            CategoryViewSet,EventViewSet,CoverImageViewSet,GenerateEventCardPdf,SubEventViewSet,UserEventViewSet

                            )

from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)





urlpatterns = [



    path('user-registration/' ,UserRegistrationView.as_view(),name='register-UserProfile'),
    path('user-login/',UserLoginView.as_view(),name='login-UserProfile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('user-update/',UserUpdateView.as_view(),name='UserProfile-update'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('user-logout/', LogoutUserView.as_view(), name='user-logout'),
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('categories/search/', CategoryViewSet.as_view({'get': 'search'}), name='category-search'),
    path('events/get-events-for-category/<int:category_id>/', EventViewSet.as_view({'get': 'get_events_for_category'}), name='event-get-events-for-category'),
    path('get-cover-image-for-category/<int:category_type>/',CoverImageViewSet.as_view({'get': 'get_cover_images_for_category_type'}), name = 'get-cover-images-for-category_type'),
    path('generate-event-card/<int:event_id>/', GenerateEventCardPdf.as_view(), name='generate-event-card'),
    path('subevents/search/', SubEventViewSet.as_view({'get': 'sub_event_search'})),
    path('subevents/get-subevents-for-events/<int:event_id>/', SubEventViewSet.as_view({'get': 'get_subevent_for_events'})),
    path('subevents/get-subevents-for-category/<int:category_id>/', SubEventViewSet.as_view({'get': 'get_subevents_for_category'})),
    path('user-events/<int:pk>/change-status/', UserEventViewSet.as_view({'patch': 'change_status'}), name='user-event-change-status')
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




