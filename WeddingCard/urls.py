from django.contrib import admin
from django.urls import include,path
from WeddingApp import views
from rest_framework.routers import DefaultRouter
from WeddingApp.views import CategoryViewSet,CoverImageViewSet,EventViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'cover-images', CoverImageViewSet, basename='coverimage')
router.register(r'events', EventViewSet, basename='events')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('WeddingApp.urls')),
    path ('auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    
]
