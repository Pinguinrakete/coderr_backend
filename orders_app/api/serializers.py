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

"""Serializer for creating an order from an offer detail."""
class CreateOrderFromOfferSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField()

    # Validate that the offer detail exists.
    def validate_offer_detail_id(self, value):
        try:
            OfferDetail.objects.get(id=value)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError("OfferDetail with this ID does not exist.")
        return value

    # Validate that only customers can create orders.
    def validate(self, data):
        user = self.context.get('request').user
        if user.user_type != Account.CUSTOMER:
            raise PermissionDenied("Only customer users can create orders.")
        return data

    # Create an order from offer detail.
    def create(self, validated_data):
        order_detail_id = validated_data["offer_detail_id"]
        user = self.context['request'].user

        order = Offer.objects.filter(details__id=order_detail_id).first()
        if not order:
            raise serializers.ValidationError("No offer found for this OfferDetail.")

        order_detail = order.details.filter(id=order_detail_id).first()
        if not order_detail:
            raise serializers.ValidationError("OfferDetail not found in this offer.")

        order = Order.objects.create(
            customer_user=user,  
            business_user=order.business_user,    
            title=order.title,
            revisions=order_detail.revisions,
            delivery_time_in_days=order_detail.delivery_time_in_days,
            price=order_detail.price,
            features=order_detail.features,
            offer_type=order_detail.offer_type,
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