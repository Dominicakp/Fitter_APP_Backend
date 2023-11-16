from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .manager import UserManager
import uuid

class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otp = models.IntegerField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save_otp(self, otp):
        self.otp = otp
        self.save()

    def compare_otp(self, otp):
        return self.otp == otp

    def __str__(self):
        return self.email