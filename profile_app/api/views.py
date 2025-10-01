from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileSingleSerializer, ProfileSinglePatchSerializer, ProfilesBusinessSerializer, ProfilesCustomerSerializer
from profile_app.models import Profile

"""Retrieve or update a single user profile."""
class ProfileSingleView(APIView):
    permission_classes = [IsAuthenticated]
    
    # Get a single profile by user ID.
    def get(self, request, pk):
        try:
            profile = Profile.objects.get(user__pk=pk)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileSingleSerializer(profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update a single profile by user ID.
    def patch(self, request, pk):
        try:
            profile = Profile.objects.get(user__pk=pk)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if profile.user != request.user:
            return Response({"detail": "You do not have permission to edit this profile."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProfileSinglePatchSerializer(profile, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            profile = serializer.save()
            return Response(ProfileSingleSerializer(profile, context={'request': request}).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""List all business user profiles."""
class ProfilesBusinessView(APIView):
    permission_classes = [IsAuthenticated]

    # Get all business profiles.
    def get(self, request):
        try:
            profiles = Profile.objects.filter(user__user_type="business")
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfilesBusinessSerializer(profiles, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


"""List all customer user profiles."""
class ProfilesCustomerView(APIView):
    permission_classes = [IsAuthenticated]

    # Get all customer profiles.
    def get(self, request):
        try:
            profiles = Profile.objects.filter(user__user_type="customer")
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfilesCustomerSerializer(profiles, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)