from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from reviews_app.models import Review
from .serializers import ReviewSerializer

class ReviewsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        try:
            if serializer.is_valid(raise_exception=True):
                review = serializer.save()
                return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewSingleView(APIView):
    pass
