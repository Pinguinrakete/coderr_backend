from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileSingleSerializer, ProfileSinglePatchSerializer, FileUploadSerializer
from profile_app.models import Profile

class ProfileSingleView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        try:
            profile = Profile.objects.get(user__pk=pk)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileSingleSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            profile = Profile.objects.get(user__pk=pk)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSinglePatchSerializer(profile, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            profile = serializer.save()
            return Response(ProfileSingleSerializer(profile, context={'request': request}).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfilesBusinessView(APIView):
    pass


class ProfilesCustomerView(APIView):
    pass


class FileUploadView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        profile_id = request.data.get('id')

    def patch(self, request, format=None):
        return self.handle_upload(request)

    def handle_upload(self, request):
        profile_id = request.data.get('id')
        if not profile_id:
            return Response({"detail": "Profil-ID not found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile = Profile.objects.get(user__pk=profile_id)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FileUploadSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)