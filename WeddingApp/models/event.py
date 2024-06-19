from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


class Event(models.Model):
    id = models.AutoField(_("ID"), primary_key=True)
    cover_image_id = models.ForeignKey('CoverImage', on_delete=models.PROTECT, related_name= 'event_cover_image')
    image = models.ImageField(upload_to='EventImages/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name = 'events_user')
    event_category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='events_category')
    additional_fields = models.JSONField(_("Fields"), null=False, default = dict())
    event_date = models.DateField(_("date"), null=True, blank=True)
    role = models.CharField(_("role"), max_length=100, blank=True, null=True)
    is_published = models.BooleanField(_("Is Published"), default=False)
    invited = models.ManyToManyField('UserProfile', related_name='shared_events', blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    is_seen = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.event_category}"

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')


