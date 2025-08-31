from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import BulkUserUploadSerializer


class BulkUserUploadView(APIView):
    permission_classes = [permissions.IsAdminUser]  # only admins can bulk add users

    def post(self, request, *args, **kwargs):
        serializer = BulkUserUploadSerializer(data=request.data)
        if serializer.is_valid():
            users, errors = serializer.create_users_from_csv(request.FILES['file'])
            return Response({
                "created": len(users),
                "errors": errors
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
