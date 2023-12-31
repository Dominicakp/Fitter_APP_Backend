from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .manager import UserManager
from django.core.validators import MaxLengthValidator, RegexValidator
import uuid

class User(AbstractUser, PermissionsMixin):
    """Custom user model with extended fields and permissions."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otp = models.IntegerField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    """
    Methods:
    - save_otp(otp): Save provided OTP to the user instance.
    - compare_otp(otp): Compare provided OTP with stored OTP for validation.
    

    Attributes:
    - otp (IntegerField): User's one-time password for verification.
    - email (EmailField): User's email address.
    """

    def save_otp(self, otp):
        self.otp = otp
        self.save()

    def compare_otp(self, otp):
        return self.otp == otp

    # - __str__(): Return the user's email as a string.
    def __str__(self):
        return self.email