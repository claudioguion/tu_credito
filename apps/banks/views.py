from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from apps.utils.permissions import IsAuthenticatedOrReadOnly
from .models import Bank
from .serializers import BankSerializer


class BankPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()

    serializer_class = BankSerializer
    pagination_class = BankPagination

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']  # Filtering by 'type' of Bank

    permission_classes = [IsAuthenticatedOrReadOnly]

