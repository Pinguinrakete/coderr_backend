from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import RegistrationSerializer, LoginSerializer
from django.db import IntegrityError
""" 
This handles the user registration. 

Method: POST
Accepts: username, email, password, repeated password, type.
Returns: saved_account data on success or validation errors.
"""
class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            try:
                saved_account = serializer.save()
                token, created = Token.objects.get_or_create(user=saved_account)
                data = {
                    'token': token.key,
                    'username': saved_account.username,
                    'email': saved_account.email,
                    'user_id': saved_account.id
                }
                return Response(data, status=status.HTTP_201_CREATED)
        
            except Exception as e:
                # Debug-Ausgabe
                return Response({'error': str(e)}, status=500)
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
"""
This handles the user login.

Method: POST
Accepts: username and password.
Returns: user data on success or authentication error.
"""
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            login_user = serializer.validated_data['user']
            login_user.last_login = timezone.now()
            login_user.save(update_fields=['last_login'])

            token, created = Token.objects.get_or_create(user=login_user)
            data = {
                'token': token.key,
                'username': login_user.username,
                'email': login_user.email,
                'user_id': login_user.id
            }
            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)