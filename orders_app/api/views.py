from django.db.models import Q
from orders_app.models import Order
from .permissions import IsStaffUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OrderSerializer, CreateOrderFromOfferSerializer, OrderSinglePatchSerializer, OrderCountSerializer

class OrdersView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):       
        orders = Order.objects.filter(Q(customer_user=request.user.customer_user)).distinct()
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
                print(traceback.format_exc()) 
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class OrderCountView(APIView):
    pass

class CompletedOrderCountView(APIView):
    pass