from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from rest_framework import viewsets, status
from rest_framework.decorators import action

from api.all_serializers.user_tg_serializers import TelegramUsersSerializer
from users.models import TelegramUsers


class TelegramUsersViewSet(viewsets.ModelViewSet):
    serializer_class = TelegramUsersSerializer
    queryset = TelegramUsers.objects.all()

    @action(
        detail=False,
        url_path=r'(?P<chat_id>\d+)/subscribe',
        methods=['get']
    )
    def is_subscribed(self, request, chat_id=None):
        user = get_object_or_404(TelegramUsers, chat_id=chat_id)
        if not user:
            return Response(
                {'Нет такого пользователя'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({'Пользователь зарегистрирован'}, status=status.HTTP_200_OK)

    @action(
        detail=False,
        url_path=r'(?P<chat_id>\d+)/delete',
        methods=['delete']
    )
    def delete_user(self, request, chat_id=None):
        user = get_object_or_404(TelegramUsers, chat_id=chat_id)
        if not user:
            return Response(
                {'Нет такого пользователя'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.delete()
        return Response({'Пользователь удален'},
                        status=status.HTTP_204_NO_CONTENT)