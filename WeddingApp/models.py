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
    id = models.AutoField(_("ID"), primary_key=True, unique=True)
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name

class CoverImage(models.Model):
    id = models.AutoField(_("ID"), primary_key=True, unique=True)
    image = models.ImageField(upload_to='covers/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])

class Event(models.Model):
    event_creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_events_user')
    event_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events_category')
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=200)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class BirthdayParty(Event):
    celebrant_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    theme = models.CharField(max_length=100)
    guest_of_honor = models.CharField(max_length=100)

class WeddingCard(Event):
    bride_name = models.CharField(max_length=100)
    groom_name = models.CharField(max_length=100)
    wedding_date = models.DateField()
    RSVP_email = models.EmailField()
    message = models.TextField()
    cover_photo = models.ImageField(upload_to='covers/', blank=True, null=True)
    rsvp_deadline = models.DateField()
   
    def __str__(self):
        return f"{self.bride_name} & {self.groom_name}'s Wedding Invitation"

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
