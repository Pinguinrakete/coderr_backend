from rest_framework import serializers
from offers_app.models import FileUpload

class ProfileSerializer(serializers.ModelSerializer):
    pass


class ProfileSinglePatchSerializer(serializers.ModelSerializer):
    pass


class ProfilesBusinessSerializer(serializers.ModelSerializer):
    pass


class ProfilesCustomerSerializer(serializers.ModelSerializer):
    pass


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['file', 'uploaded_at']