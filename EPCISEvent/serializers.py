from rest_framework import serializers
from .models import EPCISEvent

class EPCISEventSerializer(serializers.ModelSerializer):
    epcis_json = serializers.SerializerMethodField()
    epcis_xml = serializers.SerializerMethodField()
    
    class Meta:
        model = EPCISEvent
        fields = '__all__'
        read_only_fields = ('event_id',)
    
    def get_epcis_json(self, obj):
        return obj.get_epcis_json()
    
    def get_epcis_xml(self, obj):
        return obj.to_epcis_xml()
