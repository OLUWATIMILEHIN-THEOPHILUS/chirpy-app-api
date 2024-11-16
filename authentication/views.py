from rest_framework import generics, status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from authentication.serializers import SignUpSerializer
from authentication.serializers import SignInSerializer

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model

from .tokens import create_jwt_pair_for_user

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import update_session_auth_hash
from authentication.serializers import ChangePasswordSerializer
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()




class SignUpView(generics.GenericAPIView):

    serializer_class = SignUpSerializer    

    @swagger_auto_schema(
        operation_summary="SignUp a User",
        operation_description="This endpoint creates/signup a new user"
    )
    def post(self, request: Request):

        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "User Created Successfully",
                "data": {
                    "user_data": serializer.data,
                    "status": status.HTTP_201_CREATED,
                }
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        
        response = {
            "message": "User Not Created",
            "error": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST,
        }
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        try:
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user    

class SignInView(generics.GenericAPIView):

    serializer_class = SignInSerializer

    @swagger_auto_schema(
        operation_summary="SignIn a User",
        operation_description="This endpoint authenticates and signin an existing user"
    )
    def post(self, request: Request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = CustomBackend().authenticate(request, username=username, password=password)

        if user is not None:

            tokens = create_jwt_pair_for_user(user)

            response = {
                "message": "User signed in successfully",
                "data": {
                    "user_data": {
                        "email": user.email,
                        "username": user.username,
                    },
                    "status": status.HTTP_200_OK,
                    "tokens": tokens,
                },
            }

            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {
                "message": "Invalid credentials",
                "status": status.HTTP_401_UNAUTHORIZED,
                }
            return Response(data=response, status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ChangePasswordSerializer

    @swagger_auto_schema(
        operation_summary="Change User's Password",
        operation_description="This endpoint allows an authenticated user to change password"
    )
    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.validated_data['old_password']):
                if serializer.data.get('new_password') != serializer.data.get('old_password'):
                    if serializer.data.get('new_password') != serializer.data.get('confirm_password'):
                        response = {
                            "message": "Password does not match",
                            "error": serializer.errors,
                            "status": status.HTTP_400_BAD_REQUEST,
                        }
                        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
                    
                    user.set_password(serializer.validated_data['new_password'])
                    user.save()
                    update_session_auth_hash(request, user)
                
                    response = {
                        "message": "Password has been changed successfully",
                        "status": status.HTTP_200_OK,
                    }
                    return Response(data=response, status=status.HTTP_200_OK)

                response = {
                            "message": "You entered your old_password",
                            "error": serializer.errors,
                            "status": status.HTTP_400_BAD_REQUEST,
                        }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                
            response = {
                "message": "Old password is incorrect",
                "error": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        response = {
            "message": "Password not changed",
            "error": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST,
        }
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
