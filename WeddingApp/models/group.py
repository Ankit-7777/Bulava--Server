from django.db import models
from .base import BaseModel

class Group(BaseModel):
    name = models.CharField(max_length=255)
    event = models.OneToOneField('Event', on_delete=models.CASCADE, related_name='group')
    member = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='group_members')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
