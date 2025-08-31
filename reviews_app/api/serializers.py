from rest_framework import serializers
from reviews_app.models import Review
from auth_app.models import Account

class ReviewSerializer(serializers.ModelSerializer):
    business_user = serializers.IntegerField(write_only=True) 
    reviewer = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def get_reviewer(self, obj):
        return obj.reviewer.customer_user if obj.reviewer.user_type == Account.CUSTOMER else None

    def create(self, validated_data):
        request = self.context['request']
        reviewer = request.user
        business_user_id = validated_data.pop('business_user')
  
        try:
            user = Account.objects.get(business_user=business_user_id, user_type=Account.BUSINESS)
        except Account.DoesNotExist:
            raise serializers.ValidationError({'business_user': 'No business account found with this ID.'})

        if user == reviewer:
            raise serializers.ValidationError("You cannot self-evaluate.")

        return Review.objects.create(
            user=user,
            reviewer=reviewer,
            **validated_data
        )

    def get_reviewer(self, obj):
        return obj.reviewer.customer_user if obj.reviewer.user_type == Account.CUSTOMER else obj.reviewer.business_user


class ReviewSinglePatchSerializer(serializers.ModelSerializer):
    pass

