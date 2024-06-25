from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from PIL import Image

class Category(models.Model):
    
    id = models.AutoField(_("Id"), primary_key=True)
    category_name = models.CharField(max_length=50, unique=True)
    category_image = models.ImageField(upload_to='CategoryImages/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png','webp'])])
    additional_fields = models.JSONField(null=False, default = dict())
    sub_category = models.BooleanField(default= False)
    category = models.ForeignKey('Category', null=True, blank=True,on_delete=models.PROTECT, related_name='Sub_category')
    
    def __str__(self):
        return self.category_name
