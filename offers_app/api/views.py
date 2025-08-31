from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from .serializers import OfferSerializer, OfferDetailsSerializer, OfferSinglePatchSerializer, ImageUploadSerializer
from offers_app.models import Offer, OfferDetail

class OffersView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = OfferSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                offer = serializer.save()
                return Response(OfferSerializer(offer).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                import traceback
                print(traceback.format_exc()) 
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferSingleView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        try:
            offer = Offer.objects.get(pk=id)
        except Offer.DoesNotExist:
            return Response({"detail": "Offer not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OfferSinglePatchSerializer(offer, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            offer = Offer.objects.get(pk=id)
        except Offer.DoesNotExist:
            return Response({"detail": "Offer not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user.id != offer.user_id:
            return Response({"detail": "Only the owner can delete this Offer."}, status=status.HTTP_403_FORBIDDEN)

        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class OfferDetailsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, id):
        try:
            offer_detail = OfferDetail.objects.get(pk=id)
        except OfferDetail.DoesNotExist:
            return Response({"detail": "OfferDetail not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OfferDetailsSerializer(offer_detail, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ImageUploadView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, format=None):
        offer_id = request.data.get('id')
        if not offer_id:
            return Response({"detail": "Image ID not found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            offer = Offer.objects.get(pk=offer_id)
        except Offer.DoesNotExist:
            return Response({"detail": "Image not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ImageUploadSerializer(offer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)