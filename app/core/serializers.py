from rest_framework import serializers
from django.contrib.auth import get_user_model
from core import models


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""

    class Meta:
        model = models.User
        fields = ('id', 'email', 'password', 'name')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Creates a new user"""
        user = models.User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            name = validated_data['name']
        )

        return user

    def update(self, instance, validated_data):
        """Handles updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)
