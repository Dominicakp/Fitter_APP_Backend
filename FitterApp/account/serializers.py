from rest_framework import serializers
from account.models import User, CustomerProfile, MechanicProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class RegSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'username']


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, style={"input_type": "password"})
    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {"required": True}
        }


    def create(self, validated_data):
        password = validated_data.pop("password")
        confirm_password = validated_data.pop("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Password and confirm Password don't match")

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        return user
    
class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=30)
    class Meta:
        model = User
        fields = ["username","password"]
        
        
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email','mobile_number','is_verified')
        
class UpdateCustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ('phone_number', 'address')

class UpdateMechanicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MechanicProfile
        fields = ('experience_years', 'specializations')