from rest_framework import serializers
from offers_app.models import Offer
from orders_app.models import Order

class OrderSerializer(serializers.ModelSerializer):
    # business_user = serializers.IntegerField(source='user.business_user')
    # customer_user = serializers.IntegerField(source='user.customer_user')

    class Meta:
        model = Order
        fields = ['id', 'title', 'status', 'created_at', 'updated_at']
        # fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']


class CreateOrderFromOfferSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField()

    def validate_offer_id(self, value):
        from offers_app.models import Offer
        try:
            offer = Offer.objects.get(id=value)
        except Offer.DoesNotExist:
            raise serializers.ValidationError("Offer does not exist.")
        return value

    def create(self, validated_data):
        print('validated_data', validated_data)
        offer_id = validated_data['offer_detail_id']
        offer = Offer.objects.get(id=offer_id)

        order = Order.objects.create(
            title=offer.title
        )
        return order

class OrderSingleSerializer(serializers.ModelSerializer):
    pass


class OrderCountSerializer(serializers.ModelSerializer):
    pass


class CompletedOrderSerializer(serializers.ModelSerializer):
    pass

