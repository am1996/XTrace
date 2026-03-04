from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'code', 'primary_gtin']
    search_fields = ['name', 'code', 'primary_gtin']
    ordering_fields = ['created_at', 'name']
