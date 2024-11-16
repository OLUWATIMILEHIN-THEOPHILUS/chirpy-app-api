from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from chirps.models import Chirp, ChirpComment, ChirpLike
from chirps.serializers import ChirpSerializer, ChirpCommentSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema

class ChirpListCreateView(generics.GenericAPIView,
                          generics.mixins.ListModelMixin,
                          generics.mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = ChirpSerializer
    queryset = Chirp.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(chirper=user)

        return super().perform_create(serializer)

    @swagger_auto_schema(
        operation_summary="List Chirps",
        operation_description="This endpoint lists all chirps made by the users"
    )
    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Chirp",
        operation_description="This endpoint allows an authenticated user to create a chirp either including media with caption or without media"
    )
    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ChirpRetrieveUpdateDeleteView(generics.GenericAPIView,
                                    generics.mixins.RetrieveModelMixin,
                                    generics.mixins.UpdateModelMixin,
                                    generics.mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = ChirpSerializer
    queryset = Chirp.objects.all()

    @swagger_auto_schema(
        operation_summary="Get a Chirp",
        operation_description="This enpoint gets a single chirp"
    )
    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Edit a Chirp",
        operation_description="This endpoint allows an authenticated user to edit a chirp created by the user"
    )
    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Delete a Chirp",
        operation_description="This endpoint allows an authenticated user to delete a chirp created by the user"
    )
    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    
class ChirpCommentCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_summary="Commnent on Chirp",
        operation_description="This endpoint allows an authenticated user to make a comment on a chirp"
    )
    def post(self, request, chirp_id):
        try:
            chirp = Chirp.objects.get(pk=chirp_id)
        except Chirp.DoesNotExist:
            response = {
                "message": "Chirp not found",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)    

        user = request.user
        data = self.request.data
        serializer = ChirpCommentSerializer(data=data)

        if serializer.is_valid():
            serializer.save(chirper=user, chirp=chirp)

            response = {
                "message": "Comment sent sucessfully",
                "status": status.HTTP_201_CREATED
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        response = {
            "message": "Comment not sent",
            "status": status.HTTP_400_BAD_REQUEST
        }

        return Response(data=[serializer.errors, response], status=status.HTTP_400_BAD_REQUEST)


class ChirpLikeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_summary="Like a Chirp",
        operation_description="This endpoint allows an authenticated user to like a chirp"
    )
    def post(self, request, chirp_id):
        try:
            chirp = Chirp.objects.get(pk=chirp_id)
        except Chirp.DoesNotExist:
            response = {
                "message": "Chirp not found",
                "status": status.HTTP_404_NOT_FOUND,
            }

            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

        chirper = request.user

        if ChirpLike.objects.filter(chirper=chirper, chirp=chirp).exists():
            response = {
                "message": "You've already liked this post",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        
        like = ChirpLike(chirper=chirper, chirp=chirp)
        like.save()

        response = {
            "message": "Chirp liked successfully",
            "status": status.HTTP_201_CREATED,
        }

        return Response(data=response, status=status.HTTP_201_CREATED)