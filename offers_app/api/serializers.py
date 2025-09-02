from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from rest_framework.fields import CurrentUserDefault
from auth_app.models import Account


class OfferDetailsSerializer(serializers.ModelSerializer):
    features = serializers.ListField(child=serializers.CharField(max_length=255), required=False, default=list)
    
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class CurrentBusinessUserDefault:
    requires_context = True

    def __call__(self, serializer_field):
        user = serializer_field.context['request'].user
        if user.user_type != Account.BUSINESS:
            raise serializers.ValidationError("Only business users can create offers.")
        return user


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True) 
    image = serializers.ImageField(required=False, allow_null=True)
    business_user = serializers.HiddenField(default=CurrentBusinessUserDefault())

    class Meta:
        model = Offer
        fields = ['user', 'title', 'image', 'description', 'details', 'business_user']
        read_only_fields = ['user']


    def create(self, validated_data):
        details_data = validated_data.pop('details')
        user = self.context['request'].user

        if user.user_type != Account.BUSINESS:
            raise serializers.ValidationError("Only business users can create offers.")
    
        validated_data['user'] = user
        validated_data['business_user'] = user

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