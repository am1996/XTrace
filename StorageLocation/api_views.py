from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import StorageLocation
from .serializers import StorageLocationSerializer

class StorageLocationViewSet(viewsets.ModelViewSet):
    queryset = StorageLocation.objects.filter(is_active=True)
    serializer_class = StorageLocationSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['location_type', 'gln', 'is_active']
    search_fields = ['name', 'gln']
    ordering_fields = ['created_at', 'name']
