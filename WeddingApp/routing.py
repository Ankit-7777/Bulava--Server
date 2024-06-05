# from WeddingCard.asgi import application
from WeddingApp.consumers import NotificationConsumer
from django.urls import path, include,re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from WeddingApp import consumers
import WeddingApp.signals

websocket_urlpatterns = [
    re_path(r'ws/notifications/(?P<user_id>\d+)/$', NotificationConsumer.as_asgi()),
]
