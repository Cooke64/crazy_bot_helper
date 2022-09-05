from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from passport import models


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='document.id')
    name = serializers.ReadOnlyField(source='document.name')
    update_date = serializers.ReadOnlyField(
        source='document.update_date'
    )

    class Meta:
        model = models.TravelOrder
        fields = ('id', 'name', 'update_date', 'visa_info')

    def to_representation(self, instance: models.TravelOrder) -> dict:
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value}


class OrderDetailSerializer(serializers.ModelSerializer):
    document_name = serializers.ReadOnlyField(source='document.name')
    country = serializers.ReadOnlyField(source='country.name')

    class Meta:
        model = models.TravelOrder
        fields = ('document_name', 'country', 'visa_info')


class DocumentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='document.id')
    name = serializers.ReadOnlyField(source='document.name')
    country_name = serializers.ReadOnlyField(source='country.name')
    image = Base64ImageField()

    class Meta:
        model = models.CountryDocument
        fields = ('id', 'name', 'country_name', 'duration', 'image',
                  'addition_information', 'is_biometric'
                  )

    def to_representation(self, instance: models.CountryDocument) -> dict:
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value}
