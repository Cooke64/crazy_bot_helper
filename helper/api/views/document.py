from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from api.all_serializers.document_serializers import DocumentSerializer
from api.filters import DocumentFilter
from passport.models import CountryDocument


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    queryset = CountryDocument.objects.all()
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('country__name', 'document__name')

