from rest_framework import serializers
from .models import SerialNumberPool

class SerialNumberPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = SerialNumberPool
        fields = '__all__'
        read_only_fields = ('pool_id', 'created_at', 'updated_at')
