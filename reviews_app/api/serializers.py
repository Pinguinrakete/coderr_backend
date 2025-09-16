from rest_framework import serializers
from auth_app.models import Account
from reviews_app.models import Review
from rest_framework.exceptions import ValidationError
from django.db.models import Q

class ReviewSerializer(serializers.ModelSerializer):
    business_user = serializers.IntegerField(min_value=1)
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)
   
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def validate(self, attrs):
        user = self.context['request'].user
        
        if user.user_type != Account.CUSTOMER:
            raise ValidationError("Only customers can leave reviews.")
        return attrs


    def validate_business_user(self, value):          
        allowed_ids = set(Account.objects.filter(business_user__isnull=False, user_type=Account.BUSINESS).values_list('business_user', flat=True))
        print('allowed_ids', allowed_ids)
        
        if value not in allowed_ids:
            raise serializers.ValidationError(f"Die ID {value} ist kein erlaubter Business-Account.")
        
        return value


    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user

        return super().create(validated_data)


class ReviewSinglePatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']