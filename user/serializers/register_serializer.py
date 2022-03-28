import datetime

from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class CustomRegisterSerializer(RegisterSerializer):
    password1 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    full_name = serializers.CharField(required=True)

    def validate_full_name(self, full_name):
        split_full_name = full_name.split(' ')
        if len(split_full_name) == 1:
            raise serializers.ValidationError(_('Please provide your first name and last name'))
        return full_name

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1',),
            'email': self.validated_data.get('email',),
            'full_name': self.validated_data.get('full_name')
        }
