from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import BusinesProfileCountSerializer
from auth_app.models import Account

class BaseInfoView(APIView):
    permission_classes = [AllowAny]
       
    def get(self, request):
        try:
            user = Account.objects.exclude(business_user=None).values_list('business_user', flat=True).distinct()
            offer_count = len(user)

            if offer_count == 0:
                return Response({"detail": "Business doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

            serializer = BusinesProfileCountSerializer({'business_profile_count': offer_count}, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)