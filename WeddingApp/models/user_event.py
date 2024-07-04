from django.db import models
from .base import BaseModel

class UserEvent(BaseModel):
    STATUS_CHOICES = (
        ('accepted', 'Accepted'),
        ('ignored', 'Ignored'),
        ('declined', 'Declined'),
    )
    guest = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='guest_events')
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='user_events')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='ignored')

    def __str__(self):
        return f"{self.guest.full_name} - {self.event.name} - {self.status}"
