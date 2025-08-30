from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from auth_app.models import Account


class OfferDetailsSerializer(serializers.ModelSerializer):
    features = serializers.ListField(child=serializers.CharField(max_length=255), required=False, default=list)

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

# class OfferDetailsWithIdSerializer(serializers.ModelSerializer):
#     features = serializers.ListField(child=serializers.CharField(max_length=255), required=False, default=list)

#     class Meta:
#         model = OfferDetail
#         fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True) 
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Offer
        fields = ['user', 'title', 'image', 'description', 'details']
        read_only_fields = ['user']

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        user = self.context['request'].user
        offer = Offer.objects.create(user=user, **validated_data)
        
        for detail_data in details_data:
            detail_obj, created = OfferDetail.objects.get_or_create(**detail_data)
            offer.details.add(detail_obj)

        return offer
    
class OfferSingleSerializer(serializers.ModelSerializer):
    pass

class OfferSinglePatchSerializer(serializers.ModelSerializer):
    pass

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['image', 'uploaded_at']