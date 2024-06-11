from django.db import models

class AppConfig(models.Model):
    message = models.TextField(max_length=255)
    business_config = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    