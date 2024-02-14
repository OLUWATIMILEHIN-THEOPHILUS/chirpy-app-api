from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        
        user.set_password(password)

        user.save()

        return user



class User(AbstractUser):
    email=models.CharField(max_length=50, unique=True)
    username=models.CharField(max_length=20, unique=True)
    phone_number=models.CharField(max_length=15)
    country=models.CharField(null=True, max_length=60)
    gender=models.CharField(null=True, max_length=10)
    date_of_birth=models.DateField(null=True)
    profile_picture=models.ImageField(null=True)
    bio=models.TextField(null=True, max_length=120)
    is_verified=models.BooleanField(null=True, blank=True, default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone_number"]

    def __str__(self) ->str:
        return self.username

