from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import default_storage
from .serializers import AvatarSerializer
from rest_framework.response import Response


class AvatarView(views.APIView):
    """Представления для операций над аватаром модели AvatarUser."""

    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        serializer = AvatarSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            if request.user.avatar:
                default_storage.delete(request.user.avatar.path)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = request.user
        if user.avatar:
            default_storage.delete(user.avatar.path)
            user.avatar = None
            user.save()
        return Response(
            {"message": "Аватар успешно удален."},
            status=status.HTTP_204_NO_CONTENT
        )
