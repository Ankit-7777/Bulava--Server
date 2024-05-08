from django.contrib import admin
from django.urls import include,path
from WeddingApp import views
from rest_framework.routers import DefaultRouter
from WeddingApp.views import CategoryViewSet,CoverImageViewSet,BirthdayPartyViewSet,WeddingEventViewSet,InaugurationEventViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'cover-images', CoverImageViewSet, basename='coverimage')
router.register(r'birthday-parties', BirthdayPartyViewSet, basename='birthday-parties')
router.register(r'weeding-events', WeddingEventViewSet, basename='wedding-events')
router.register(r'inaugration-events', InaugurationEventViewSet, basename='inaugration-events')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('WeddingApp.urls')),
    path ('auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    
]
