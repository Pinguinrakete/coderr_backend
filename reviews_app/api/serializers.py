from rest_framework import serializers
from auth_app.models import Account
from reviews_app.models import Review
from rest_framework.exceptions import ValidationError
from django.db.models import Q

"""
Serializer for creating and retrieving reviews.

Fields:
- id (int, read-only): Review ID.
- business_user (int): ID of the reviewed business user.
- reviewer (int, read-only): ID of the user leaving the review (auto-assigned).
- rating (int): Value from 1 to 5.
- description (str): Optional review content.
- created_at / updated_at (datetime, read-only): Timestamps.

Validations:
- Only users with `user_type="customer"` may create reviews.
- `business_user` must be a valid business account (ID must exist in allowed set).

On creation:
- Reviewer is automatically set to the authenticated user.
"""
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
        if value not in allowed_ids:
            raise serializers.ValidationError(f"Die ID {value} ist kein erlaubter Business-Account.")
        
        return value


    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user

        return super().create(validated_data)

"""
Serializer for partial updates to a review.

Fields:
- id (int, read-only): Review ID.
- rating (int): Updated rating (1–5).
- description (str): Updated review text.
- created_at / updated_at (datetime, read-only): Timestamps.

Usage:
- Used in PATCH requests to update the `rating` and/or `description` of an existing review.
"""
class ReviewSinglePatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']