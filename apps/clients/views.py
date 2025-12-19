from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from apps.utils.permissions import IsAuthenticatedOrReadOnly
from .models import Client
from .serializers import ClientSerializer
from .filters import ClientFilter


class ClientPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()

    serializer_class = ClientSerializer
    pagination_class = ClientPagination

    # Filters
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ClientFilter
    search_fields = ['full_name']

    permission_classes = [IsAuthenticatedOrReadOnly]
