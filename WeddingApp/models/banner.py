from django.db import models
from django.core.validators import FileExtensionValidator
from PIL import Image


class BannerImage(models.Model):
    image = models.ImageField(upload_to='banners/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png','webp', 'gif', 'bmp', 'tiff', 'svg', 'ico'])])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    def __str__(self):
        return self.image.name if self.image else "No Image"

    def save(self, *args, **kwargs):
        super(BannerImage, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 1000 or img.width > 1000:
            output_size = (1000, 1000)
            img.thumbnail(output_size)
            img.save(self.image.path)
