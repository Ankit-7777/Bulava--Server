from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

class RSVP(models.Model):
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='rsvps')
    guest = models.ForeignKey("Guest", on_delete=models.CASCADE, related_name='rsvps')
    response = models.CharField(max_length=10, choices=(('Yes', 'Yes'), ('No', 'No'), ('Maybe', 'Maybe')))
