import random
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
import os


def send_otp_email(user):
    """
    This sends a randomly generated 6-digit OTP code to the user's email for verification.
    """

    # Generate a random 6-digit OTP code
    otp_code = random.randint(100000, 999999)

    # Save the OTP code to the user model's otp field
    user.otp = otp_code
    user.save()  


    # Send the OTP code via email
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp_code}'
    from_email = os.environ.get('EMAIL_USER')
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
    
"""
    Sends an OTP email when a new user is created.
"""    
@receiver(post_save, sender=User)
def send_otp_on_registration(sender, instance, created, **kwargs):
    if created:
        # Send OTP email when a new user is created
        send_otp_email(instance)