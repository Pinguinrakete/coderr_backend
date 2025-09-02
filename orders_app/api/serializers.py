from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order

class OrderSerializer(serializers.ModelSerializer):
    # business_user = serializers.IntegerField(source='user.business_user')
    # customer_user = serializers.IntegerField(source='user.customer_user')

    class Meta:
        model = Order
        fields = ['id', 'title', 'revisions', 'price', 'delivery_time_in_days', 'created_at', 'updated_at']
        # fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'status, 'created_at', 'updated_at']


class CreateOrderFromOfferSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField()

    def validate_offer_detail_id(self, value):
        try:
            OfferDetail.objects.get(id=value)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError("OfferDetail with this ID does not exist.")
        return value

    def create(self, validated_data):
        offer_detail_id = validated_data["offer_detail_id"]

        offer = Offer.objects.filter(details__id=offer_detail_id).first()
        if not offer:
            raise serializers.ValidationError("No offer found for this OfferDetail.")

        offer_detail = offer.details.filter(id=offer_detail_id).first()
        if not offer_detail:
            raise serializers.ValidationError("OfferDetail not found in this offer.")

        order = Order.objects.create(
            title=offer.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
        )
        return order

class OrderSingleSerializer(serializers.ModelSerializer):
    pass


class OrderCountSerializer(serializers.ModelSerializer):
    pass


class CompletedOrderSerializer(serializers.ModelSerializer):
    pass

