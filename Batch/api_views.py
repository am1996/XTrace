from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Batch
from .serializers import BatchSerializer

class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['batch_number', 'product']
    search_fields = ['batch_number', 'order_number']
    ordering_fields = ['created_at', 'manufactured_at']
