from django.urls import path
from account.views import *

urlpatterns = [
    # Endpoint for user registration
    path("register/", RegistrationView.as_view(), name="register"),
    # Endpoint for OTP verification during user registration
    path('verify-otp/', OTPVerificationView.as_view(), name='otp-verification'),
    # Endpoint for user login
    path("login/", LoginView.as_view(), name="login"),
    # URL pattern for updating user profiles
    path('update-profile/', UpdateUserProfileView.as_view(), name='update-profile'),
]