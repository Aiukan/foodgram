"""Представления subscriptions."""
from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Subscription
from .serializers import SubscriptionsSerializer

User = get_user_model()


class SubscriptionView(APIView):
    """Вьюсет модели Subscription."""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        """Подписка на пользователя."""
        user_from = request.user
        user_to = get_object_or_404(User, id=id)
        if user_from == user_to:
            return Response(
                {"error": "Нельзя подписаться на себя."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Subscription.objects.filter(
            user_from=user_from, user_to=user_to
        ).exists():
            return Response(
                {"error": "Подписка уже осуществлена."},
                status=status.HTTP_400_BAD_REQUEST
            )
        Subscription.objects.create(user_from=user_from, user_to=user_to)
        serializer = SubscriptionsSerializer(
            user_to,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        """Отписка от пользователя."""
        user_to = get_object_or_404(User, id=id)
        subscription_entry = Subscription.objects.filter(
            user_from=request.user,
            user_to=user_to
        )
        if not subscription_entry.exists():
            return Response(
                {'error': 'Подписка на данного пользователя не найдена.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        subscription_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionListView(ListAPIView):
    """Представление для списка подписок."""

    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionsSerializer

    def get_queryset(self):
        """Получение всех подписок пользователя."""
        user = self.request.user
        if not user.is_authenticated:
            return User.objects.none()
        return User.objects.filter(Exists(Subscription.objects.filter(
            user_from=user, user_to=OuterRef('id')
        )))
