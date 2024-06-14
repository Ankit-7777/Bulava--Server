from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from WeddingApp.views import (
    CategoryViewSet,
    CoverImageViewSet,
    EventViewSet,
    ContectUsViewSet,
    AppConfigViewSet,
)
from WeddingApp import views


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'cover-images', CoverImageViewSet, basename='coverimage')
router.register(r'events', EventViewSet, basename='events')
router.register(r'contact-us', ContectUsViewSet, basename='contact-us')
router.register(r'app_config', AppConfigViewSet, basename='app_config')

urlpatterns = [
    
    path('', views.index, name='index'), 
    path('admin/', admin.site.urls),
    path('', include('WeddingApp.urls')),
    path('auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    
    path('birthday/', views.birthday, name='birthday'),
    path('inaugurations/', views.inaugrations, name='inaugrations'),
    path('wedding/', views.wedding, name='wedding'),
    path('custom/', views.custom, name='custom'),
      
]
