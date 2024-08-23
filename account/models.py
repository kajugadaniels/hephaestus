from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from account.managers import *

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Director', 'Director'),
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
    )

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    
    added_by = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='added_users')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name', 'email']

    def __str__(self):
        return self.email