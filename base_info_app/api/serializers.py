from rest_framework import serializers

class BusinesProfileCountSerializer(serializers.Serializer):
    business_profile_count = serializers.IntegerField()