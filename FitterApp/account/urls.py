from django.urls import path
from account.views import *

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path('verify-otp/', OTPVerificationView.as_view(), name='otp-verification'),
     path("login/", LoginView.as_view(), name="login"),
]