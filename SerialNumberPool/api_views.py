from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import SerialNumberPool
from .serializers import SerialNumberPoolSerializer

class SerialNumberPoolViewSet(viewsets.ModelViewSet):
    queryset = SerialNumberPool.objects.all()
    serializer_class = SerialNumberPoolSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'generated_by']
    ordering_fields = ['created_at']
