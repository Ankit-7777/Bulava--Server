from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


class Device(models.Model):
    app_label = "Device"
    db_table = "device"

    IOS = 'ios'
    ANDROID = 'android'

    STATUS_CHOICE = [
        (IOS, IOS),
        (ANDROID, ANDROID),
    ]
    
    user = models.ForeignKey("UserProfile",  on_delete=models.CASCADE, related_name="devices")
    device_id = models.CharField(max_length=125)
    type = models.CharField(max_length=50, choices=STATUS_CHOICE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __str__(self):
        return self.device_id