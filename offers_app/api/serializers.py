from auth_app.models import Account
from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from rest_framework.reverse import reverse

"""Serializer for offer detail objects."""
class OfferDetailsSerializer(serializers.ModelSerializer):
    features = serializers.ListField(child=serializers.CharField(max_length=255), required=False, default=list)
    
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

"""Serializer for creating and validating offers."""
class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True) 
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
        read_only_fields = ['id']

    # Validate that at least 3 offer details are provided.
    def validate(self, data):
        if 'details' in data and len(data['details']) < 3:
            raise serializers.ValidationError({'details': 'At least 3 offer details are required.'})
        return data

    # Create an offer with related details.
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        user = self.context['request'].user

        if user.user_type != Account.BUSINESS:
            raise serializers.ValidationError("Only business users can create offers.")
    
        validated_data['user'] = user
        offer = Offer.objects.create(**validated_data)
        
        for detail_data in details_data:
            detail_obj = OfferDetail.objects.create(**detail_data)
            offer.details.add(detail_obj)
            
        return offer

"""Serializer for minimal offer detail representation."""
class OfferDetailMiniSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    # Return URL for offer detail.
    def get_url(self, obj):
        request = self.context.get('request')
        return reverse('offer-detail', args=[obj.id], request=request)


"""Serializer for user details in offers."""
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username']


"""Serializer for listing offers with summary info."""
class OfferListSerializer(serializers.ModelSerializer):
    details = OfferDetailMiniSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = UserDetailsSerializer(source='user')

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']

    # Get minimum price from offer details.
    def get_min_price(self, obj):
        prices = obj.details.values_list('price', flat=True)
        return min(prices) if prices else None

    # Get minimum delivery time from offer details.
    def get_min_delivery_time(self, obj):
        times = obj.details.values_list('delivery_time_in_days', flat=True)
        return min(times) if times else None

"""Serializer for a single offer with summary info."""
class OfferListSingleSerializer(serializers.ModelSerializer):
    details = OfferDetailMiniSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']

    # Get minimum price from offer details.
    def get_min_price(self, obj):
        prices = obj.details.values_list('price', flat=True)
        return min(prices) if prices else None

    # Get minimum delivery time from offer details.
    def get_min_delivery_time(self, obj):
        times = obj.details.values_list('delivery_time_in_days', flat=True)
        return min(times) if times else None
    

"""Serializer for updating an offer and its details."""
class OfferSinglePatchSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True) 
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Offer
        fields = ['title', 'image', 'description', 'details']
        read_only_fields = ['user']

    # Update offer and its related details.
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

"""Serializer for uploading or updating offer images."""
class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['image', 'uploaded_at']