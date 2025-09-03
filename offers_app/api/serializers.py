from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from auth_app.models import Account
from django.contrib.auth.models import User


class OfferDetailsSerializer(serializers.ModelSerializer):
    features = serializers.ListField(child=serializers.CharField(max_length=255), required=False, default=list)
    
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True) 
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
        read_only_fields = ['id']

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        user = self.context['request'].user

        if user.user_type != Account.BUSINESS:
            print('welcher User bist du?', user.user_type)
            raise serializers.ValidationError("Only business users can create offers.")
    
        validated_data['user'] = user
        validated_data['business_user'] = user.business_user

        offer = Offer.objects.create(**validated_data)
        
        for detail_data in details_data:
            detail_obj = OfferDetail.objects.create(**detail_data)
            offer.details.add(detail_obj)
            
        return offer


class OfferSinglePatchSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True) 
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Offer
        fields = ['title', 'image', 'description', 'details']
        read_only_fields = ['user']

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            instance.details.clear()

            for detail_data in details_data:
                detail_obj, _ = OfferDetail.objects.get_or_create(**detail_data)
                instance.details.add(detail_obj)

        return instance

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['image', 'uploaded_at']