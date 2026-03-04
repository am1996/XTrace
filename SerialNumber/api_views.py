from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import SerialNumber
from .serializers import SerialNumberSerializer

class SerialNumberViewSet(viewsets.ModelViewSet):
    queryset = SerialNumber.objects.all()
    serializer_class = SerialNumberSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'pool', 'batch_lot']
    search_fields = ['full_serial_number', 'batch_lot']
    ordering_fields = ['last_modified']
