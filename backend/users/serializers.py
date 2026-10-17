"""Serializers for the users app."""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'role', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Public-safe user serializer."""

    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'role', 'is_active', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """JWT token serializer that also returns user info."""

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'full_name': self.user.full_name,
            'role': self.user.role,
        }
        return data
