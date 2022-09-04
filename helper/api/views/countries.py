from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.all_serializers.passport_serializers import CountryListSerializer
from api.filters import CountryFilter
from passport import models
from passport.models import FavoriteCountryTG, Country
from users.models import TelegramUsers


class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountryListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CountryFilter
    queryset = models.Country.objects.all()

    @action(
        detail=False,
        url_path=r'(?P<pk>\d+)/subs/(?P<chat_id>\d+)',
        methods=['get', 'post', 'delete']
    )
    def subscriptions_list(self, request, pk=None, chat_id=None):
        user = get_object_or_404(TelegramUsers, chat_id=chat_id)
        country = get_object_or_404(Country, pk=pk)
        queryset = FavoriteCountryTG.objects.filter(user=user, country=country)
        if self.request.method == 'GET':
            return Response(status=status.HTTP_201_CREATED if queryset.exists() else status.HTTP_200_OK)
        if self.request.method == 'POST':
            if queryset.exists():
                return Response(
                    {'message': 'Вы уже подписаны'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            FavoriteCountryTG.objects.create(
                user=user,
                country=country
            )
            return Response(
                {'message': 'Подписались:)'},
                status=status.HTTP_201_CREATED,
            )
        if not queryset.exists():
            return Response(
                {'message': 'Вы не подписаны на данную страну'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset.delete()
        return Response(
            {'message': 'Отписались:('},
            status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        url_path=r'(?P<pk>\d+)/(?P<chat_id>\d+)',
        methods=['post']
    )
    def update_last_seen(self, request, pk=None, chat_id=None):
        query = TelegramUsers.objects.get(chat_id=chat_id)
        query.country_last_seen_pk = pk
        query.save()
        return Response({pk})

    @action(
        detail=False,
        url_path=r'(?P<chat_id>\d+)',
        methods=['get']
    )
    def get_last_seen(self, request, chat_id=None):
        query = TelegramUsers.objects.get(chat_id=chat_id)
        return Response({query.country_last_seen_pk})

