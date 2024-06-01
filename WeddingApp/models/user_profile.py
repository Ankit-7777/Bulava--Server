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
    image = models.ImageField(_("Image"),upload_to='UserProfile/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
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
