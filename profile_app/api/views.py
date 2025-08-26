from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileSingleSerializer, ProfileSinglePatchSerializer, FileUploadSerializer
from profile_app.models import Profiles

class ProfileSingleView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        try:
            profile = Profiles.objects.get(user__pk=pk)

        except Profiles.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileSingleSerializer(profile, context={'request': request})
        print('serializer.data: ', serializer.data)
        return Response(serializer.data)


    def patch(self, request, pk):
        try:
            profile = Profiles.objects.get(user__pk=pk)
            print('profile: ', profile)
        except Profiles.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSinglePatchSerializer(profile, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            profile = serializer.save()
            return Response(ProfileSinglePatchSerializer(profile, context={'request': request}).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfilesBusinessView(APIView):
    pass


class ProfilesCustomerView(APIView):
    pass

class FileUploadView(APIView):
    def post(self, request, format=None):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)