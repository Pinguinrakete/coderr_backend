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

        if details_data is not None:
            existing_detail_ids = {detail.id for detail in instance.details.all()}

            for detail_data in details_data:
                detail_id = detail_data.get('id')

                if detail_id:
                    try:
                        detail_obj = OfferDetail.objects.get(id=detail_id)
                        if detail_obj.id not in existing_detail_ids:
                            raise serializers.ValidationError(
                                f"OfferDetail with id {detail_id} does not belong to this offer."
                            )

                        for attr, value in detail_data.items():
                            setattr(detail_obj, attr, value)
                        detail_obj.save()

                    except OfferDetail.DoesNotExist:
                        raise serializers.ValidationError(
                            f"OfferDetail with id {detail_id} not found."
                        )
                else:
                    detail_obj = OfferDetail.objects.create(**detail_data)
                    instance.details.add(detail_obj)

        return instance

"""The serializer's response includes the update offer and its details."""
class OfferSinglePatchResponseSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True, read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']
        read_only_fields = ['id', 'details']