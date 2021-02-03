from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'mobile_number', 'role']


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10, min_length=3, required=True)
    password = serializers.CharField(max_length=20, min_length=5, required=True)


class ChangeUserPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=15, min_length=5)
    new_password = serializers.CharField(max_length=15, min_length=5)
    confirm_password = serializers.CharField(max_length=15, min_length=5)


class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20)
    confirm_password = serializers.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['password', 'confirm_password']