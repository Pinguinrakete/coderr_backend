from django.db.models import Q
from orders_app.models import Order
from .permissions import IsStaffUser
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OrderSerializer, CreateOrderFromOfferSerializer, OrderSinglePatchSerializer, OrderCountSerializer, CompletedOrderSerializer
from django.contrib.auth.models import User
from auth_app.models import Account

"""
Handles listing and creation of orders.

Permissions:
- Allows any user (authenticated or not) to access.

Methods:

GET:
- Retrieves orders where the requesting user is either the customer or business user.
- Returns a serialized list of orders.

POST:
- Creates a new order from provided data.
- Uses CreateOrderFromOfferSerializer for validation and creation.
- Returns the created order data on success.

Errors:
- 400 on validation errors.
- 500 on unexpected server errors with error detail.
"""
class OrdersView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):      
        orders = Order.objects.filter(Q(customer_user=request.user.customer_user) | Q(business_user=request.user.business_user)).distinct()
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = CreateOrderFromOfferSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                order = serializer.save()
                return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                import traceback
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
Handles partial update and deletion of a single order.

Permissions:
- PATCH: Requires authenticated user.
- DELETE: Requires staff user.
- Other methods: default permissions.

Methods:

PATCH:
- Partially updates an order by its primary key.
- Returns the updated order data on success.
- 400 on validation errors.
- 404 if the order does not exist.

DELETE:
- Deletes an order by its primary key.
- 204 on successful deletion.
- 404 if the order does not exist.
"""
class OrderSingleView(APIView):
    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [IsStaffUser()]
        return super().get_permissions()

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
    
    def delete(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
Returns the count of in-progress orders for a specific business user.

Permissions:
- Requires authentication.

GET:
- Path parameter: business_user_id (int) — ID of the business user.
- Checks if the business user exists.
- Returns the count of orders with status 'in_progress' for the given business user.

Errors:
- 404 if the business user does not exist.
"""
class OrderCountView(APIView):
    permission_classes = [IsAuthenticated]
       
    def get(self, request, business_user_id): 
        try:
            Account.objects.get(business_user=business_user_id)
        except Account.DoesNotExist:
            return Response({"detail": "A business user with this ID does not exist."}, status=status.HTTP_404_NOT_FOUND)

        orders = Order.objects.filter(Q(business_user=business_user_id) & Q(status="in_progress")).distinct()
        count_in_progress = len(orders)
        serializer = OrderCountSerializer({'order_count': count_in_progress}, context={'request': request})

        return Response(serializer.data)
    
"""
Returns the count of completed orders for a specific business user.

Permissions:
- Requires authentication.

GET:
- Path parameter: business_user_id (int) — ID of the business user.
- Validates existence of the business user.
- Returns the count of orders with status 'completed' for the specified business user.

Errors:
- 404 if the business user does not exist.
"""
class CompletedOrderCountView(APIView):
    permission_classes = [IsAuthenticated]
       
    def get(self, request, business_user_id): 
        try:
            Account.objects.get(business_user=business_user_id)
        except Account.DoesNotExist:
            return Response({"detail": "A business user with this ID does not exist."}, status=status.HTTP_404_NOT_FOUND)

        orders = Order.objects.filter(Q(business_user=business_user_id) & Q(status="completed")).distinct()
        count_completed = len(orders)
        serializer = CompletedOrderSerializer({'completed_order_count': count_completed}, context={'request': request})

        return Response(serializer.data)