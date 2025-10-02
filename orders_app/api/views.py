from django.db.models import Q
from orders_app.models import Order
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OrderSerializer, CreateOrderFromOfferSerializer, OrderSinglePatchSerializer, OrderCountSerializer, CompletedOrderSerializer
from auth_app.models import Account

"""List or create orders for the authenticated user."""
class OrdersView(APIView):
    permission_classes = [IsAuthenticated]
    
    # List all orders for the current user.
    def get(self, request):
        user = request.user
        
        orders = Order.objects.filter(Q(customer_user=user) | Q(business_user=user)).distinct()
        
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)
    
    # Create a new order from an offer.
    def post(self, request):
        serializer = CreateOrderFromOfferSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                order = serializer.save()
                return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""Update or delete a single order."""
class OrderSingleView(APIView):
    permission_classes = [IsAuthenticated]

    # Update a single order by ID.
    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSinglePatchSerializer(order, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order, context={'request': request}).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete a single order by ID (admin only).
    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response({"detail": "Only admin users can delete orders."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""Get count of in-progress orders for a business user."""
class OrderCountView(APIView):
    permission_classes = [IsAuthenticated]
       
    # Return count of in-progress orders for a business user.
    def get(self, request, business_user_id):
        try:
            Account.objects.get(business_user=business_user_id)
        except Account.DoesNotExist:
            return Response({"detail": "A business user with this ID does not exist."}, status=status.HTTP_404_NOT_FOUND)

        orders = Order.objects.filter(Q(business_user=business_user_id) & Q(status="in_progress")).distinct()
        count_in_progress = len(orders)
        serializer = OrderCountSerializer({'order_count': count_in_progress}, context={'request': request})

        return Response(serializer.data)
    
"""Get count of completed orders for a business user."""
class CompletedOrderCountView(APIView):
    permission_classes = [IsAuthenticated]
       
    # Return count of completed orders for a business user.
    def get(self, request, business_user_id):
        try:
            Account.objects.get(business_user=business_user_id)
        except Account.DoesNotExist:
            return Response({"detail": "A business user with this ID does not exist."}, status=status.HTTP_404_NOT_FOUND)

        orders = Order.objects.filter(Q(business_user=business_user_id) & Q(status="completed")).distinct()
        count_completed = len(orders)
        serializer = CompletedOrderSerializer({'completed_order_count': count_completed}, context={'request': request})

        return Response(serializer.data)