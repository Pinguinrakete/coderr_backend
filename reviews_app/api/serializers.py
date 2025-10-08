from rest_framework import serializers
from auth_app.models import Account
from reviews_app.models import Review
from rest_framework.exceptions import PermissionDenied, ValidationError

"""Serializer for creating and validating reviews."""
class ReviewSerializer(serializers.ModelSerializer):
    business_user = serializers.PrimaryKeyRelatedField(queryset=Account.objects.filter(user_type=Account.BUSINESS))
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)
   
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    # Validate that only customers can leave reviews.
    def validate(self, attrs):
        user = self.context['request'].user
        
        if user.user_type != Account.CUSTOMER:
            raise PermissionDenied("Only authenticated users with a customer profile are allowed to submit reviews.")
        
        business_user_id = attrs.get('business_user', None)

        if Review.objects.filter(reviewer=user, business_user=business_user_id).exists():
            raise PermissionDenied("You have already reviewed this business profile.")
        return attrs

    # Validate that business_user is a valid business account.        
    def validate_business_user(self, value):
        if value.user_type != Account.BUSINESS:
            raise serializers.ValidationError("The selected user is not a business account.")
        return value

    # Set reviewer to the current user.
    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user

        return super().create(validated_data)

"""Serializer for updating a review."""
class ReviewSinglePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'business_user', 'reviewer', 'created_at', 'updated_at']