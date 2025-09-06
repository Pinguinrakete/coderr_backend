from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

class BaseInfoView(APIView):
    permission_classes = [AllowAny]
       
    def get(self, request):
        try:
            profiles = Profile.objects.filter(user__user_type="business")
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfilesBusinessSerializer(profiles, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
