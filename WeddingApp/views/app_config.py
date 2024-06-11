from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from WeddingApp.models import AppConfig
from WeddingApp.serializers.app_config import AppConfigSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class AppConfigViewSet(viewsets.ModelViewSet):
    queryset = AppConfig.objects.all()
    serializer_class = AppConfigSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def list(self, request):
        app_config = AppConfig.objects.first()
        serializer = AppConfigSerializer(app_config)
        return Response(serializer.data, status=status.HTTP_200_OK)
