from rest_framework import generics, status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from authentication.serializers import SignUpSerializer

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpView(generics.GenericAPIView):

    serializers_class = SignUpSerializer    

    def post(self, request: Request):

        data = request.data

        serializer = self.serializers_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "User Created Successfully",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def get(self, request: Request):
        
        response = {
            "user": str(request.user),
        }

        return Response(data=response, status=status.HTTP_200_OK)

    def post(self, request: Request):

        # username_or_email = request.data.get('username_or_email')
        # password = request.data.get('password')
        # user = CustomBackend().authenticate(request=request, username=username_or_email, password=password)

        username = request.data.get('username') 
        password = request.data.get('password')

        user = CustomBackend().authenticate(request, username=username, password=password)

        if user is not None:
            response = {
                "message": "User signed in successfully",
                "data": [user.username, user.email]
            }

            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {
                "message": "Invalid credentials"
                }
            return Response(data=response, status=status.HTTP_401_UNAUTHORIZED)

