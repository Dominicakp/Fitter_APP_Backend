from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .manager import UserManager
from django.core.validators import MaxLengthValidator, RegexValidator
import uuid

class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10,15}$',  # Adjust the regex to match your phone number format
                message='Username must be a valid Mobile Number',
                code='invalid_username'
            )
        ]
    )
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otp = models.IntegerField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "mobile_number" 
    REQUIRED_FIELDS = ["email"]

    def save_otp(self, otp):
        self.otp = otp
        self.save()

    def compare_otp(self, otp):
        return self.otp == otp

    def __str__(self):
        return self.email 
