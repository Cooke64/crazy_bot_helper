from rest_framework import serializers

from api.all_serializers.document_serializers import OrderSerializer, \
    OrderDetailSerializer
from passport import models


class CountryListSerializer(serializers.ModelSerializer):
    moving_order = serializers.SerializerMethodField()

    class Meta:
        model = models.Country
        fields = ('pk', 'name', 'is_friendly', 'moving_order')

    def get_moving_order(self, obj: models.Country) -> dict:
        request = self.context.get('request')
        try:
            orders = request.GET['orders']
            if orders:
                queryset = models.TravelOrder.objects.filter(
                    country=obj, document__pk=request.GET['orders']
                )
                return OrderDetailSerializer(queryset, many=True).data
        except KeyError:
            queryset = models.TravelOrder.objects.filter(country=obj)
            return OrderSerializer(queryset, many=True).data


class CountryDocumentDetailSerializer(serializers.ModelSerializer):
    pass
