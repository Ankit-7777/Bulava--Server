from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from WeddingApp.models import Event

@receiver(post_save, sender=Event)
def send_event_notification(sender, instance, created, **kwargs):
    if created:
        user_id = instance.user.id
        group_name = f"user_{user_id}"
        notification_message = f"A new event '{instance.title}' has been created."

        print(f"Sending notification to group {group_name}: {notification_message}")

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "notification_message",
                "message": notification_message,
                "event_id": instance.id
            }
        )
