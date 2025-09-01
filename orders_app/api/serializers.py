from rest_framework import serializers
from orders_app.models import Order

class OrderSerializer(serializers.ModelSerializer):
    business_user = serializers.IntegerField(source='user.business_user')
    customer_user = serializers.IntegerField(source='user.customer_user')

    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at']


class CreateOrderFromOfferSerializer(serializers.ModelSerializer):
    pass


class OrderSingleSerializer(serializers.ModelSerializer):
    pass


class OrderCountSerializer(serializers.ModelSerializer):
    pass


class CompletedOrderSerializer(serializers.ModelSerializer):
    pass

