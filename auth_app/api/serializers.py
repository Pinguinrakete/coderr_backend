from auth_app.models import Account
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from profile_app.models import Profiles

"""
This handles user registration serializers.

Method: POST  
Accepts: username, email, password, repeated_password, type.  
Returns: saved account data on success or validation errors.
"""
class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True, required=True)
    type = serializers.ChoiceField(source='user_type', choices=Account.USER_TYPE_CHOICES, required=True)

    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})

        if Account.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'A user with this username already exists.'})

        if Account.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'A user with this email already exists.'})

        return data

    def create(self, validated_data):
        validated_data.pop('repeated_password')
        user = Account.objects.create_user(**validated_data)
        Profiles.objects.create(user=user)

        return user
    
""" 
This serializer handles the user login process. 

- Expects: username and password.
- Authenticates user credentials.
- Raises error if authentication fails.
"""
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'password']

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)  
        if user is None:
            raise serializers.ValidationError(_("Username or password is invalid"))

        data['user'] = user
        return data