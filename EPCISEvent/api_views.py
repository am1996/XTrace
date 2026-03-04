from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from .models import EPCISEvent
from .serializers import EPCISEventSerializer

class EPCISEventViewSet(viewsets.ModelViewSet):
    queryset = EPCISEvent.objects.all()
    serializer_class = EPCISEventSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['event_type', 'action', 'biz_step']
    search_fields = ['biz_step', 'disposition']
    ordering_fields = ['event_time']
    
    @action(detail=True, methods=['get'])
    def json(self, request, pk=None):
        event = self.get_object()
        return Response(event.get_epcis_json(), content_type='application/json')
    
    @action(detail=True, methods=['get'])
    def xml(self, request, pk=None):
        event = self.get_object()
        return HttpResponse(event.to_epcis_xml(), content_type='application/xml')
