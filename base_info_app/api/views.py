from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import BaseInfoSerializer
from auth_app.models import Account
from offers_app.models import Offer
from reviews_app.models import Review

class BaseInfoView(APIView):
    permission_classes = [AllowAny]
       
    def get(self, request):
        try:
            review_count = Review.objects.count()
            business_user_count = Account.objects.exclude(business_user=None).count()
            offer_count = Offer.objects.count() 

            serializer = BaseInfoSerializer(
                    {
                        'review_count': review_count,
                        'business_profile_count': business_user_count,
                        'offer_count': offer_count 
                    }, 
                    context={'request': request}
                )
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)