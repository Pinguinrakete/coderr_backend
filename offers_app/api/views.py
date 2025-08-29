from offers_app.models import Offer
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from .serializers import OfferSerializer, OfferSingleSerializer, OfferSinglePatchSerializer, OfferDetailsSerializer

class OffersView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            serializer = OfferSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                board = serializer.save()
            return Response(OfferSerializer(board, context={'request': request}).data, status=status.HTTP_201_CREATED)
        
        except Offer.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferSingleView(APIView):
    pass


class OfferDetailsView(APIView):
    pass
