from rest_framework import serializers

from api.all_serializers.document_serializers import OrderDetailSerializer
from passport.models import FavoriteCountryTG


class FavoriteTgSerializer(serializers.ModelSerializer):
    country_name = serializers.ReadOnlyField(source='country.name')
    visa_info = OrderDetailSerializer(source='country.travelorder_set', read_only=True, many=True)

    class Meta:
        model = FavoriteCountryTG
        fields = ('country_name', 'visa_info')


class FavoritePkAndNameSerializer(serializers.ModelSerializer):
    country_name = serializers.ReadOnlyField(source='country.name')
    country_pk = serializers.ReadOnlyField(source='country.pk')

    class Meta:
        model = FavoriteCountryTG
        fields = ('country_pk', 'country_name', 'url')