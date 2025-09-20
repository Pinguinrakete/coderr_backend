from rest_framework import serializers

"""
Serializer for returning general platform statistics.

Fields:
- review_count (IntegerField): Total number of user reviews submitted on the platform.
- average_rating (DecimalField): Average rating from all reviews. Format: max 2 digits, 1 decimal place.
- business_profile_count (IntegerField): Number of registered business user profiles.
- offer_count (IntegerField): Total number of service offers available on the platform.
"""
class BaseInfoSerializer(serializers.Serializer):
    review_count = serializers.IntegerField()
    average_rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    business_profile_count = serializers.IntegerField()
    offer_count = serializers.IntegerField()