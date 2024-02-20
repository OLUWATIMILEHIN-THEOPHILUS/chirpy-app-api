from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from authentication.serializers import SignUpSerializer

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

    

