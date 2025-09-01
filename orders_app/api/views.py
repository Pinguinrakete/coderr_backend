from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OrderSerializer, CreateOrderFromOfferSerializer
from offers_app.models import Offer, OfferDetail

class OrdersView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        serializer = CreateOrderFromOfferSerializer(data=request.data)
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
    pass


class OrderCountView(APIView):
    pass


class CompletedOrderCountView(APIView):
    pass