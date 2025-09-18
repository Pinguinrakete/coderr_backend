from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from auth_app.models import Account

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer_user','business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']


class CreateOrderFromOfferSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField()

    def validate_offer_detail_id(self, value):
        try:
            OfferDetail.objects.get(id=value)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError("OfferDetail with this ID does not exist.")
        return value

    def validate(self, data):
        user = self.context.get('request').user
        if user.user_type != Account.CUSTOMER:
            raise serializers.ValidationError("Only customer users can create offers.")
        return data

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
            user=user,
            customer_user=user.customer_user,
            business_user=order.business_user,
            title=order.title,
            revisions=order_detail.revisions,
            delivery_time_in_days=order_detail.delivery_time_in_days,
            price=order_detail.price,
            features=order_detail.features,
            offer_type=order_detail.offer_type,
        )
        return order


class OrderSinglePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
        read_only_fields = ['id', 'customer_user','business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'created_at', 'updated_at']

    def validate(self, data):
        user = self.context.get('request').user
        if user.user_type != Account.CUSTOMER:
            raise serializers.ValidationError("Only customer users can update offers.")
        return data
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class OrderCountSerializer(serializers.Serializer):
    order_count = serializers.IntegerField()


class CompletedOrderSerializer(serializers.Serializer):
    completed_order_count = serializers.IntegerField()

