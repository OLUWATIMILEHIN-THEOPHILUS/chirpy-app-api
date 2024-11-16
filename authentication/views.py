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

User = get_user_model()




class SignUpView(generics.GenericAPIView):

    serializer_class = SignUpSerializer    

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

class SignInView(APIView):

    serializer_class = SignInSerializer

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

