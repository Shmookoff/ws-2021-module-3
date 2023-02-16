from django.core.validators import MaxLengthValidator, MinLengthValidator
from rest_framework import serializers

from .models import User


class RegisterRequest(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        # exclude = ("pk",)


class LoginRequest(serializers.Serializer):
    phone = serializers.CharField(
        validators=[MinLengthValidator(11), MaxLengthValidator(11)]
    )
    password = serializers.CharField()


class UserResponse(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)
