from auth_app.models import Account
from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from rest_framework.reverse import reverse

"""Serializer for offer detail objects."""
class OfferDetailsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    features = serializers.ListField(child=serializers.CharField(max_length=255), required=False, default=list)
    
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
    
    # Format the price to an integer if it has no decimal part.
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get('price') is not None:
            price = data['price']
            if float(price).is_integer():
                data['price'] = int(float(price))
        return data

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

    # Return image URL if present.
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

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
        return int(min(prices)) if prices else None

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
        return int(min(prices)) if prices else None

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
        fields = ['id', 'title', 'image', 'description', 'details']
        read_only_fields = ['id', 'user']

    # The validate_details function checks a list of detail dictionaries to ensure that each one contains both an 'id' and an 'offer_type' key
    def validate_details(self, value):
        offer_types = [item.get('offer_type') for item in value]
        if len(set(offer_types)) != len(offer_types):
            raise serializers.ValidationError("Duplicate offer_type values are not allowed.")
        for detail in value:
            if 'offer_type' not in detail:
                raise serializers.ValidationError("Each detail must include its 'offer_type'.")
        return value

    # Update offer and its related details.
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        user = self.context['request'].user

        if user.user_type != Account.BUSINESS:
            raise serializers.ValidationError("Only business users can create offers.")

        # Update main offer fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle detail updates based on offer_type
        if details_data is not None:
            details_by_type = {detail.offer_type: detail for detail in instance.details.all()}

            for detail_data in details_data:
                offer_type = detail_data.get('offer_type')

                if offer_type not in details_by_type:
                    raise serializers.ValidationError(
                        f"OfferDetail with offer_type '{offer_type}' does not belong to this offer."
                    )

                detail_obj = details_by_type[offer_type]

                for attr, value in detail_data.items():
                    if attr != 'offer_type':  
                        setattr(detail_obj, attr, value)
                detail_obj.save()

        return instance

"""The serializer's response includes the update offer and its details."""
class OfferSinglePatchResponseSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True, read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
        read_only_fields = ['id', 'details']