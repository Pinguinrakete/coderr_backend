from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from offers_app.models import Offer
from auth_app.models import Account
from rest_framework.exceptions import PermissionDenied

"""Serializer for order objects."""
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer_user','business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']

    # Format the price as a number (int if no decimals, else float).
    def to_representation(self, instance):
        data = super().to_representation(instance)
        price = data.get('price')
        if price is not None:
            if float(price).is_integer():
                data['price'] = int(float(price))
            else:
                data['price'] = float(price)
        return data
    
"""Serializer for creating an order from an offer detail."""
class CreateOrderFromOfferSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField()

    def validate_offer_detail_id(self, value):
        if not OfferDetail.objects.filter(id=value).exists():
            raise serializers.ValidationError("OfferDetail with this ID does not exist.")
        return value

    def validate(self, data):
        user = self.context.get('request').user
        if user.user_type != Account.CUSTOMER:
            raise PermissionDenied("Only customer users can create orders.")
        return data

    def create(self, validated_data):
        offer_detail_id = validated_data["offer_detail_id"]
        user = self.context['request'].user

        offer = Offer.objects.filter(details__id=offer_detail_id).first()
        if not offer:
            raise serializers.ValidationError("No offer found for this OfferDetail.")

        offer_detail = offer.details.filter(id=offer_detail_id).first()
        if not offer_detail:
            raise serializers.ValidationError("OfferDetail not found in this offer.")
        
        order = Order.objects.create(
            customer_user=user,  
            business_user=offer,    
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
        )
        return order

"""Serializer for updating order status."""
class OrderSinglePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
        read_only_fields = ['id', 'customer_user','business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'created_at', 'updated_at']

    # Validate that only business users can update orders.
    def validate(self, data):
        user = self.context.get('request').user
        if user.user_type != Account.BUSINESS:
            raise serializers.ValidationError("Only business users can update orders.")
        return data
       
    # Update order instance with new data.
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

"""Serializer for returning order count."""
class OrderCountSerializer(serializers.Serializer):
    order_count = serializers.IntegerField()


"""Serializer for returning completed order count."""
class CompletedOrderSerializer(serializers.Serializer):
    completed_order_count = serializers.IntegerField()