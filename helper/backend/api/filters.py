from django_filters import rest_framework as rest_framework_filter
import django_filters

from passport.models import Country, CountryDocument


class CountryFilter(rest_framework_filter.FilterSet):

    class Meta:
        model = Country
        fields = ('name', 'orders')


class DocumentFilter(rest_framework_filter.FilterSet):
    name = django_filters.CharFilter(
        field_name='document__name',
        lookup_expr='icontains',
    )
    country_name = django_filters.CharFilter(
        field_name='country__name',
        lookup_expr='icontains',
    )

    class Meta:

        model = CountryDocument
        fields = ('name', 'country_name')

