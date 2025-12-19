from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from apps.utils.permissions import IsAuthenticatedOrReadOnly
from .models import Credit
from .serializers import CreditSerializer


class CreditPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class CreditViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all()

    serializer_class = CreditSerializer
    pagination_class = CreditPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["description", "client__full_name", "bank__name"]
    filterset_fields = ["credit_type", "bank", "client"]

    permission_classes = [IsAuthenticatedOrReadOnly]
