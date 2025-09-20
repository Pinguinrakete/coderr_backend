from rest_framework import serializers
from profile_app.models import Profile

"""
Serializes profile with related user info.

Fields: user ID, username, name, file URL, location, contact, description, user type, email, created date.

All fields read-only.
"""
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

    def get_file(self, obj):
        if obj.file:
            return obj.file.url
        return None

"""
Serializer for partial updates to a user's profile and basic account data.

Fields (all optional):
- first_name, last_name, email (from user)
- file, location, tel, description, working_hours (from profile)

Updates:
- Applies changes to both Profile and related User model.
"""
class ProfileSinglePatchSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)  
    email = serializers.EmailField(source='user.email', required=False)
    file = serializers.FileField(required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'email']

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

"""
Serializes basic profile info for business users.

Includes:
- user ID, username, name, file URL, contact info, description, working hours, and user type.

All fields are read-only.
"""
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

    def get_file(self, obj):
        if obj.file:
            return obj.file.url
        return None

"""
Serializes basic profile info for customer users.

Includes:
- user ID, username, name, file URL, upload time, and user type.

All fields are read-only.
"""
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

    def get_file(self, obj):
        if obj.file:
            return obj.file.url
        return None
    
"""
Serializer for uploading a file to a user's profile.

Fields:
- file (FileField): The uploaded file.
- uploaded_at (DateTimeField): Timestamp of the upload.
"""
class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['file', 'uploaded_at']