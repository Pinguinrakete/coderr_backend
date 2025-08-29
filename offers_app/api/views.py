from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from .serializers import OfferSerializer

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
                print(traceback.format_exc())  # Zeigt Fehler im Terminal
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferSingleView(APIView):
    pass


class OfferDetailsView(APIView):
    pass
