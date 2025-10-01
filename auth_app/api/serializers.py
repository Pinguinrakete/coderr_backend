from auth_app.models import Account
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from profile_app.models import Profile


"""Serializer for user registration."""
class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True, required=True)
    type = serializers.ChoiceField(source='user_type', choices=Account.USER_TYPE_CHOICES, required=True)

    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

    # Validate registration data.
    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})

        if Account.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'A user with this username already exists.'})

        if Account.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'A user with this email already exists.'})

        return data

    # Create user and profile.
    def create(self, validated_data):
        validated_data.pop('repeated_password')
        user = Account.objects.create_user(**validated_data)
        Profile.objects.create(user=user)

        return user
    

"""Serializer for user login."""
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'password']

    # Validate login credentials.
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)  
        if user is None:
            raise serializers.ValidationError(_("Username or password is invalid"))

        data['user'] = user
        return data