from rest_framework import serializers
from .models import StorageLocation

class StorageLocationSerializer(serializers.ModelSerializer):
    epcis_uri = serializers.ReadOnlyField()
    
    class Meta:
        model = StorageLocation
        fields = '__all__'
        read_only_fields = ('created_at',)
