from rest_framework import serializers
from profile_app.models import Profile

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


class ProfileSinglePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'description', 'email']


class ProfilesBusinessSerializer(serializers.ModelSerializer):
    pass


class ProfilesCustomerSerializer(serializers.ModelSerializer):
    pass
