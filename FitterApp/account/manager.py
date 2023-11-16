from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, phone_number=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        
        # Check if either username or phone_number is provided
        if not username and not phone_number:
            raise ValueError(_('Either username or phone_number must be set'))

        # Ensure phone_number consists only of digits
        if phone_number and not phone_number.isdigit():
            raise ValueError(_('Phone number must contain only digits'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, username=None, phone_number=None, **extra_fields):
        # Ensure that either username or phone_number is provided for a superuser
        if not username and not phone_number:
            raise ValueError(_('Either username or phone_number must be set for a superuser'))

        # Ensure phone_number consists only of digits
        if phone_number and not phone_number.isdigit():
            raise ValueError(_('Phone number must contain only digits'))

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be staff'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be superuser'))
        if extra_fields.get('is_verified') is not True:
            raise ValueError(_('Superuser must be verified'))

        user = self.create_user(email, password, username=username, phone_number=phone_number, **extra_fields)
        # Set is_admin attribute to True
        user.is_admin = True
        # Set is_staff attribute to True
        user.is_staff = True
        user.save()

        return user