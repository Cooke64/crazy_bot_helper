from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from api.all_serializers.favorite_serializers import FavoriteTgSerializer, \
    FavoritePkAndNameSerializer
from passport import models
from passport.models import FavoriteCountryTG
from users.models import TelegramUsers


class FavoriteTgSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteTgSerializer
    queryset = FavoriteCountryTG.objects.all()
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        url_path=r'(?P<chat_id>\d+)/get_list',
        methods=['get']
    )
    def subscriptions_list(self, request, chat_id=None):
        user = get_object_or_404(TelegramUsers, chat_id=chat_id)
        data = FavoriteCountryTG.objects.filter(user=user)
        for i in data:
            print(i.country.name)
        pages = self.paginate_queryset(data)
        serializer = FavoritePkAndNameSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
