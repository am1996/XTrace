from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Equipment
from .serializers import EquipmentSerializer

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.filter(deleted_at__isnull=True)
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['plant_gln', 'manufacturer']
    search_fields = ['name', 'model_number', 'serial_number']
    ordering_fields = ['created_at', 'name']
