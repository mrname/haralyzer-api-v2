from django.shortcuts import render
from rest_framework import viewsets

from .models import Scan
from .serializers import ScanSerializer

class ScanViewSet(viewsets.ModelViewSet):
    queryset = Scan.objects.all().order_by('-created')
    serializer_class = ScanSerializer
