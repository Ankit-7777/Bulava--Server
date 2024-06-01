from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


class Event(models.Model):
    id = models.AutoField(_("ID"), primary_key=True)
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name = 'events_user')
    event_category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='events_category')
    email = models.EmailField(_("Email"))
    guest_of_honor = models.CharField(_("Guest of Honor"), max_length=100, blank=True, null=True)
    organizer_name = models.CharField(_("Organizer Name"), max_length=100, blank=True, null=True)
    phone_number = models.CharField(_("Phone Number"), max_length=10, help_text=_("Please provide organizer's contact number."))
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"), max_length=1000, blank=True, null=True)
    event_date = models.DateField(_("Event Date"))
    event_start_time = models.TimeField(_("Event Start Time"))
    event_end_time = models.TimeField(_("Event End Time"))
    venue_name = models.CharField(_("Venue Name"), max_length=200, blank=True, null=True)
    venue_address = models.CharField(_("Venue Address"), max_length=200)
    venue_pin_code = models.CharField(_("Venue Pin Code"), max_length=6)
    is_published = models.BooleanField(_("Is Published"), default=False)
    max_guests = models.PositiveIntegerField(_("Maximum Guests"), default=100, blank=True, null=True)
    gift_sending_link = models.URLField(_("Gift Sending Link"), max_length=200, blank=True, null=True)
    theme = models.CharField(_("Theme"), max_length=100, blank=True, null=True)
    dress_code = models.CharField(_("Dress Code"), max_length=50, blank=True, null=True)
    # Wedding Specific Fields
    bride_name = models.CharField(_("Bride's Name"), max_length=100, blank=True, null=True)
    groom_name = models.CharField(_("Groom's Name"), max_length=100, blank=True, null=True)
    bride_mother_name = models.CharField(_("Bride's Mother Name"),max_length=100, blank=True, null=True)
    bride_father_name = models.CharField(_("Bride's Father Name"),max_length=100, blank=True, null=True)
    groom_mother_name = models.CharField(_("Groom's Mother Name"),max_length=100, blank=True, null=True)
    groom_father_name = models.CharField(_("Groom's Father Name"),max_length=100, blank=True, null=True)
    bride_age = models.PositiveIntegerField(_("Bride's Age"), blank=True, null=True)
    groom_age = models.PositiveIntegerField(_("Groom's Age"), blank=True, null=True)
    # Birthday Specific Fields
    birthday_person_name = models.CharField(_("Birthday Person's Name"), max_length=100, blank=True, null=True)
    birthday_person_age = models.PositiveIntegerField(_("Birthday Person's Age"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    #Notification Specific Fields
    is_seen = models.BooleanField(null=True, default=False)
    def __str__(self):
        return f"{self.title} ({self.event_category})"

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')


