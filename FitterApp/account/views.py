import random
from rest_framework.response import Response
from account.serializers import *
from rest_framework import status, generics
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from account.models import User

# JWT for Users
def get_tokens_for_user(user):

    """Generate access and refresh tokens for a given user."""

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegistrationView(APIView):
    """
        This handles a user registration through a POST request.

        Returns:
        Response: Which is user data and a success message if registration is successful.
    """
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save() # This will call the custom create method and not save it to the database

            userreg_serializer = RegSerializer(user) # serialize the user object

            return Response({
                "user": userreg_serializer.data,
                "msg": "OTP code was sent to your Email."
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def verify_otp(otp_code, user):
    """
    This verify if the provided OTP code matches the expected OTP code for a user.
    """

    # Retrieve the expected OTP code from the user model
    expected_otp_code = user.otp

    # Compare the provided OTP code with the expected OTP code
    if str(otp_code) == str(expected_otp_code):
        return True
    else:
        return False
    

class OTPVerificationView(APIView):
    """
    OTP verification for user registration.
    """
    def post(self, request, format=None):
        """
        This validates provided OTP for User registration.

        Returns:
        Response: The confirmation message and status code after OTP's verification.

        """
        otp_code = request.data.get('otp_code')
        user_id = request.data.get('user_id')

        if not otp_code or not user_id:
            return Response({"message": "Invalid OTP verification data."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"message": "Invalid user ID."}, status=status.HTTP_400_BAD_REQUEST)

        # Perform OTP verification here using your chosen method
        if not verify_otp(otp_code, user):
            return Response({"message": "Invalid OTP code."}, status=status.HTTP_400_BAD_REQUEST)

        # Set the user's is_verified attribute to True
        user.is_verified = True
        user.save()

        return Response({"message": f"Registration completed successfully. Welcome {user.username}"}, status=status.HTTP_200_OK)
    


class UpdateUserProfileView(generics.RetrieveUpdateAPIView):
    """
    A view that allows users (both customers and mechanics) to view and update their profiles.
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user
        if hasattr(user, 'customer_profile'):
            return UpdateCustomerProfileSerializer
        elif hasattr(user, 'mechanic_profile'):
            return UpdateMechanicProfileSerializer
        return UpdateUserSerializer

    def get_object(self):
        user = self.request.user
        if hasattr(user, 'customer_profile'):
            return user.customer_profile
        elif hasattr(user, 'mechanic_profile'):
            return user.mechanic_profile
        return user
    
    

class LoginView(APIView):
    """
    This is a user login view.

    Methods:
    - post: This handles HTTP POST requests for user login.
    """
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        """
        Handles user login.

        Returns:
        Response: The user data, token, and login status.
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Extracting username and password from the validated data.
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            # Attempt to authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_verified:
                # User authentication successful and verified.
                userlog_serializer = UserLogSerializer(user)
                token = get_tokens_for_user(user)
                return Response({"user": userlog_serializer.data, "token": token, "msg": "Login Successful"}, status=status.HTTP_200_OK)
            elif user is not None and not user.is_verified:
                # User authentication successful, but not verified.
                return Response({"errors": {"non_field_errors": ["User is not verified."]}}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                # failure authentication.
                return Response({"errors": {"non_field_errors": ["Username or password is not valid."]}}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
