from rest_framework import serializers
from profile_app.models import Profile
import os

"""Serializer for retrieving a single user profile."""
class ProfileSingleSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')    
    file = serializers.SerializerMethodField()
    type = serializers.CharField(source='user.user_type')
    email = serializers.EmailField(source='user.email')
    created_at = serializers.DateTimeField(source='user.date_joined')

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file','location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']
        read_only_fields = fields

    # Return file URL if present.
    def get_file(self, obj):
        if obj.file:
            return obj.file.url
        return None

"""Serializer for updating a single user profile."""
class ProfileSinglePatchSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)  
    email = serializers.EmailField(source='user.email', required=False)
    file = serializers.FileField(required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'email']

    # Validate uploaded file size.
    def validate_file(self, value):
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("The file must not be larger than 5 MB.")
        return value
    
    # Return file name if present.
    def get_file(self, obj):
        if obj.file:
            return os.path.basename(obj.file.name)
        return None
    
    # Update profile and related user fields.
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        return instance

"""Serializer for listing business user profiles."""
class ProfilesBusinessSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')    
    file = serializers.SerializerMethodField()
    type = serializers.CharField(source='user.user_type')

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type']
        read_only_fields = fields

    # Return file URL if present.
    def get_file(self, obj):
        if obj.file:
            return obj.file.url
        return None

"""Serializer for listing customer user profiles."""
class ProfilesCustomerSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')    
    file = serializers.SerializerMethodField()
    type = serializers.CharField(source='user.user_type')

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'uploaded_at', 'type']
        read_only_fields = fields

    # Return file URL if present.
    def get_file(self, obj):
        if obj.file:
            return obj.file.url
        return None