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

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    
class ChirpCommentCreateView(APIView):
     permission_classes = [IsAuthenticated]
     authentication_classes = [JWTAuthentication]

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