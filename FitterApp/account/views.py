import random
from rest_framework.response import Response
from account.serializers import *
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from account.models import User

# JWT for Users
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegistrationView(APIView):
    renderer_classes = [UserRenderer]