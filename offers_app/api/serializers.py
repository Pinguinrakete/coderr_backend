from auth_app.models import Account
from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from rest_framework.reverse import reverse

"""
Serializer for OfferDetail model.

Fields:
- id, title, revisions, delivery_time_in_days, price, offer_type
- features: optional list of feature strings (default: empty list)
"""
class OfferDetailsSerializer(serializers.ModelSerializer):
    features = serializers.ListField(child=serializers.CharField(max_length=255), required=False, default=list)
    
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

"""
Serializer for Offer model with nested offer details.

Fields:
- id (read-only)
- title
- image (optional)
- description
- details (list of nested OfferDetailsSerializer)

Notes:
- Only business users can create offers; others get a validation error.
- Creates related OfferDetail instances when creating an Offer.
"""
class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True) 
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
        read_only_fields = ['id']

    def validate(self, data):
        if 'details' in data and len(data['details']) < 3:
            raise serializers.ValidationError({'details': 'At least 3 offer details are required.'})
        return data

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        user = self.context['request'].user

        if user.user_type != Account.BUSINESS:
            raise serializers.ValidationError("Only business users can create offers.")
    
        validated_data['user'] = user
        validated_data['business_user'] = user.business_user

        offer = Offer.objects.create(**validated_data)
        
        for detail_data in details_data:
            detail_obj = OfferDetail.objects.create(**detail_data)
            offer.details.add(detail_obj)
            
        return offer

"""
Minimal serializer for OfferDetail.

Fields:
- id
- url: URL to the offer detail's API endpoint (e.g., /offerdetails/<id>/)
"""
class OfferDetailMiniSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse('offer-detail', args=[obj.id], request=request)

"""
Serializer for basic user details.

Fields:
- first_name
- last_name
- username
"""
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username']

"""
Serializer for listing offers with summary details.

Fields:
- id, user, title, image, description, created_at, updated_at
- details: list of minimal offer details (OfferDetailMiniSerializer)
- min_price: lowest price among the offer details
- min_delivery_time: shortest delivery time among the offer details
- user_details: basic user info (UserDetailsSerializer)
"""
class OfferListSerializer(serializers.ModelSerializer):
    details = OfferDetailMiniSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = UserDetailsSerializer(source='user')

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']

    def get_min_price(self, obj):
        prices = obj.details.values_list('price', flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        times = obj.details.values_list('delivery_time_in_days', flat=True)
        return min(times) if times else None

"""
Serializer for a single offer with summarized details.

Fields:
- id, user, title, image, description, created_at, updated_at
- details: list of minimal offer details (OfferDetailMiniSerializer)
- min_price: lowest price among the offer details
- min_delivery_time: shortest delivery time among the offer details
"""
class OfferListSingleSerializer(serializers.ModelSerializer):
    details = OfferDetailMiniSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']

    def get_min_price(self, obj):
        prices = obj.details.values_list('price', flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        times = obj.details.values_list('delivery_time_in_days', flat=True)
        return min(times) if times else None
    
"""
Serializer for partial updates of an Offer.

Fields:
- title
- image (optional)
- description
- details (list of OfferDetailsSerializer)

Notes:
- The user field is read-only.
- Updates offer fields and replaces related offer details.
- Existing details are cleared and new ones added (created if needed).
"""
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

"""
Serializer for uploading or updating an offer's image.

Fields:
- image: The image file.
- uploaded_at: Timestamp of the upload.
"""
class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['image', 'uploaded_at']