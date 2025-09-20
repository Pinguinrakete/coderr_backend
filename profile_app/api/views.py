from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileSingleSerializer, ProfileSinglePatchSerializer, ProfilesBusinessSerializer, ProfilesCustomerSerializer, FileUploadSerializer
from profile_app.models import Profile

"""
Handles retrieval and partial update of a user profile.

Permissions:
- AllowAny (no authentication required).

GET /profiles/<pk>/:
- Retrieves the profile linked to the user with primary key `pk`.
- Returns 404 if profile not found.

PATCH /profiles/<pk>/:
- Partially updates the profile of the user with primary key `pk`.
- Returns 404 if profile not found.
- Validates and saves partial updates.
- Returns validation errors with status 400 if invalid.
"""
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

"""
Handles retrieval of all business user profiles.

Permissions:
- AllowAny (no authentication required).

GET /profiles/business/:
- Returns a list of profiles where the linked user has user_type 'business'.
- If no profiles found, returns 404 with a relevant message.
"""
class ProfilesBusinessView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            profiles = Profile.objects.filter(user__user_type="business")
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfilesBusinessSerializer(profiles, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

"""
Handles retrieval of all customer user profiles.

Permissions:
- AllowAny (no authentication required).

GET /profiles/customer/:
- Returns a list of profiles where the linked user has user_type 'customer'.
- If no profiles found, returns 404 with a relevant message.
"""
class ProfilesCustomerView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            profiles = Profile.objects.filter(user__user_type="customer")
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfilesCustomerSerializer(profiles, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

"""
Handles partial updates for uploading files to a user's profile.

Permissions:
- AllowAny (no authentication required).

PATCH /file-upload/:
- Expects 'id' in request data representing the user’s profile ID.
- Finds the profile linked to the given user ID.
- Returns 400 if 'id' is missing.
- Returns 404 if profile not found.
- Partially updates the profile (e.g., uploads a file).
- Returns validation errors with status 400 if invalid.
"""
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