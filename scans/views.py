from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import viewsets

from .models import Scan
from .serializers import ScanSerializer


class ScanFilter(filters.FilterSet):
    class Meta:
        model = Scan
        fields = {
            'hostname': ['exact'],
            'result__total_load_time': ['lte', 'gte'],
        }


class ScanViewSet(viewsets.ModelViewSet):
    queryset = Scan.objects.all().order_by('-created')
    serializer_class = ScanSerializer
    filterset_class = ScanFilter
