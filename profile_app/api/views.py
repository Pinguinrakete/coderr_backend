from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileSingleSerializer, ProfileSinglePatchSerializer, ProfilesBusinessSerializer, ProfilesCustomerSerializer, FileUploadSerializer
from profile_app.models import Profile

class ProfileSingleView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        try:
            profile = Profile.objects.get(user__pk=pk)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileSingleSerializer(profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            profiles = Profile.objects.filter(user__user_type="business")
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfilesBusinessSerializer(profiles, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfilesCustomerView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            profiles = Profile.objects.filter(user__user_type="customer")
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfilesCustomerSerializer(profiles, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class FileUploadView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, format=None):
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