from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.core.validators import FileExtensionValidator
from PIL import Image
from django.core.exceptions import ValidationError

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, confirm_password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password=password, **extra_fields)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(_("Id"), primary_key=True)
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(_("Full Name"), max_length=255)
    phone = models.CharField(_("Phone"), max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(_("Role"), max_length=10, default='User')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone']

    objects = MyUserManager()

    def __str__(self):
        return self.full_name

    def change_password(self, new_password):
        self.password = make_password(new_password)
        self.save()

class Category(models.Model):
    id = models.AutoField(_("Id"), primary_key=True)
    category_name = models.CharField(max_length=50, unique=True)
    additional_fields = models.JSONField(null=False, default = dict())
    def __str__(self):
        return self.category_name

class CoverImage(models.Model):
    id = models.AutoField(_("ID"), primary_key=True, unique=True)
    image = models.ImageField(upload_to='covers/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    event_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events_category_type')
    
    def __str__(self):
        return f"Theme CoverImage"

class Event(models.Model):
    id = models.AutoField(_("ID"), primary_key=True)
    event_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events_category')
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

    def __str__(self):
        return f"{self.title} ({self.event_category})"

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

class Guest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='guests')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(blank=True, null=True)
    is_attending = models.BooleanField(default=False)
    dietary_restrictions = models.TextField(blank=True, null=True)

class RSVP(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='rsvps')
    response = models.CharField(max_length=10, choices=(('Yes', 'Yes'), ('No', 'No'), ('Maybe', 'Maybe')))

class Vendor(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='vendors')
    name = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

class ContactUs(models.Model):
    id = models.AutoField(_("Id"),primary_key=True)
    name = models.CharField(_("Name"), max_length=100,  null=False)
    email = models.EmailField(_("Email"),null=False)
    message = models.TextField(_("Message"), max_length=300,null=False)

