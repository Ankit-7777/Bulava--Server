import json
import logging
import asyncio
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from time import sleep
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer,JsonWebsocketConsumer
from WeddingApp.models import Event




# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user_id = self.scope['url_route']['kwargs']['user_id']
#         self.group_name = f"user_{self.user_id}"
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()
    
#     async def disconnect(self, close_code):
#         if hasattr(self, 'group_name'):
#             await self.channel_layer.group_discard(
#                 self.group_name,
#                 self.channel_name
#             )
    
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         event_id = text_data_json.get('event_id')
        
#         if event_id:
#             user_id = self.get_event_user_id(event_id)
#             if user_id:
#                 self.group_name = f"user_{user_id}"
                
#                 await self.channel_layer.group_send(
#                     self.group_name,
#                     {
#                         'type': 'notification_message',
#                         'message': text_data_json['message']
#                     }
#                 )
    
#     async def notification_message(self, event):
#         await self.send(text_data=json.dumps({
#             'message': event['message']
#         }))
    
#     def get_event_user_id(self, event_id):
#         try:
#             event = Event.objects.get(pk=event_id)
#             return event.user.id
#         except Event.DoesNotExist:
#             return None


# class NotificationConsumer(JsonWebsocketConsumer):
#     def connect(self):
#         self.user_id = self.scope['url_route']['kwargs']['user_id']
#         self.group_name = f"user_{self.user_id}"
#         async_to_sync(self.channel_layer.group_add)(
#             self.group_name,
#             self.channel_name
#         )
#         self.accept()

#     def disconnect(self, close_code):
#         if hasattr(self, 'group_name'):
#             async_to_sync(self.channel_layer.group_discard)(
#                 self.group_name,
#                 self.channel_name
#             )

#     def receive_json(self, content):
#         event_id = content.get('event_id')
        
#         if event_id:
#             user_id = self.get_event_user_id(event_id)
#             if user_id:
#                 self.group_name = f"user_{user_id}"
                
#                 async_to_sync(self.channel_layer.group_send)(
#                     self.group_name,
#                     {
#                         'type': 'notification_message',
#                         'message': content['message']
#                     }
#                 )

#     def notification_message(self, event):
#         self.send_json({
#             'message': event['message']
#         })

#     def get_event_user_id(self, event_id):
#         try:
#             event = Event.objects.get(pk=event_id)
#             return event.user.id
#         except Event.DoesNotExist:
#             return None


class NotificationConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f"user_{self.user_id}"
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )

    def receive_json(self, content):
        event_id = content.get('event_id')
        
        if event_id:
            user_id = self.get_event_user_id(event_id)
            if user_id:
                self.group_name = f"user_{user_id}"
                
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name,
                    {
                        'type': 'notification_message',
                        'message': content['message']
                    }
                )
                
                # Mark the event as seen
                self.mark_event_as_seen(event_id)

    def notification_message(self, event):
        self.send_json({
            'message': event['message']
        })
        event_id = event.get('event_id')
        if event_id:
            self.mark_event_as_seen(event_id)

    def get_event_user_id(self, event_id):
        try:
            event = Event.objects.get(pk=event_id)
            return event.user.id
        except Event.DoesNotExist:
            return None

    def mark_event_as_seen(self, event_id):
        try:
            event = Event.objects.get(pk=event_id)
            event.is_seen = True
            event.save()
        except Event.DoesNotExist:
            pass