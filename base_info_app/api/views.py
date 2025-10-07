from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import BaseInfoSerializer
from auth_app.models import Account
from offers_app.models import Offer
from reviews_app.models import Review

"""Provides base statistics for the platform."""
class BaseInfoView(APIView):
    permission_classes = [AllowAny]
       
    # Return review, rating, business profile, and offer counts.
    def get(self, request):
        try:
            review_count = Review.objects.count()
            rating_list = Review.objects.values_list('rating', flat=True)
            business_user_count = Account.objects.filter(user_type=Account.BUSINESS).count()
            offer_count = Offer.objects.count() 

            average_rating = sum(rating_list) / len(rating_list) if rating_list else 0

            serializer = BaseInfoSerializer(
                    {
                        'review_count': review_count,
                        'average_rating': average_rating,
                        'business_profile_count': business_user_count,
                        'offer_count': offer_count 
                    }, 
                    context={'request': request}
                )
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)