from rest_framework import serializers
from offers_app.models import FileUpload

class OffersSerializer(serializers.ModelSerializer):
    pass


class OfferSingleSerializer(serializers.ModelSerializer):
    pass


class OfferSinglePatchSerializer(serializers.ModelSerializer):
    pass


class OfferDetailsSerializer(serializers.ModelSerializer):
    pass

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['file', 'uploaded_at']