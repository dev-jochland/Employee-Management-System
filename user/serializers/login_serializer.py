from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class CustomLoginSerializer(LoginSerializer):
    username = None
    password = serializers.CharField(style={'input_type': 'password'})
    email = serializers.EmailField(required=True)
