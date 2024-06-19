from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

class SubEvent(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey("Category", related_name='subcategories', on_delete=models.PROTECT)
    event = models.ForeignKey("Event", related_name = "event", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='SubEventCategoryImages/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])
    additional_fields = models.JSONField(null=False, default=dict())
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)


    def __str__(self):
        return self.name