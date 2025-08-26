from rest_framework import serializers
from auth_app.models import Account
from profile_app.models import Profiles, FileUpload

class ProfileSingleSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    type = serializers.CharField(source='user.user_type')
    email = serializers.EmailField(source='user.email')
    created_at = serializers.DateTimeField(source='user.date_joined')

    class Meta:
        model = Profiles
        fields = ['user', 'username', 'first_name', 'last_name', 'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']
        read_only_fields = ['user', 'username', 'first_name', 'last_name', 'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']


class ProfileSinglePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = ['user', 'username', 'first_name', 'last_name', 'description', 'email']


class ProfilesBusinessSerializer(serializers.ModelSerializer):
    pass


class ProfilesCustomerSerializer(serializers.ModelSerializer):
    pass


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['file', 'uploaded_at']