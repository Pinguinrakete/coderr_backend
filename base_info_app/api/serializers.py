from rest_framework import serializers

""" Serializer for rounded. """
class RoundedFloatField(serializers.FloatField):
    def to_representation(self, value):
        rounded = round(float(value), 1)
        return rounded

""" Serializer for base platform statistics. """
class BaseInfoSerializer(serializers.Serializer):
    review_count = serializers.IntegerField()
    average_rating = RoundedFloatField()
    business_profile_count = serializers.IntegerField()
    offer_count = serializers.IntegerField()
