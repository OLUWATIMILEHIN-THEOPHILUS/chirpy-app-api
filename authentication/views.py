from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from authentication.serializers import SignUpSerializer

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

    

