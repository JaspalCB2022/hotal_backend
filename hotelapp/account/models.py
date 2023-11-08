from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

import uuid
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from restaurant.models import Restaurant


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role="user", **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, role="superadmin", **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, role, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ("superadmin", "Superadmin"),
        ("user", "User"),
        ('restaurant', 'Restaurant'),
        ('kitchen_staff', 'Kitchen_staff')
    )
   
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default="user")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone_number = models.CharField(null=True, blank=True, max_length=15)
    avatar = models.ImageField(
        upload_to="avatar/%Y/%m/%d/",
        null=True,
        blank=True,
    )
    
    password_reset_token = models.UUIDField(null=True, blank=True, unique=True)
    token_create_at = models.DateTimeField(null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,blank=True,null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.email)

    def generate_password_reset_token(self):
        """
        Generate a unique password reset token for the user.
        """
        token = uuid.uuid4()
        self.password_reset_token = token
        self.token_create_at = timezone.now()
        self.save()
        return token

