from typing import Any
from django.shortcuts import render
from django.views.generic import *
from Equipment.models import Equipment
# Create your views here.

class EquipmentIndex(ListView):
    model = Equipment
    template_name = "index.html"
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["equipment_list"] = Equipment.objects.filter(deleted_at__isnull=True)
        return context
    
class EquipmentDetails(DetailView):
    model = Equipment
    context_object_name = "equipment"
    template_name = "details.html"

class EquipmentUpdate(UpdateView):
    model = Equipment
    fields = ['name', 'serial_number', 'manufacturer', 'mac_address', 'ip_address', 'plant_name', 'plant_gln', 'location']
    template_name = "update.html"
    success_url = '/web/equipment/' 

class EquipmentCreate(CreateView):
    model = Equipment
    fields = ['name', 'serial_number', 'manufacturer', 'mac_address', 'ip_address', 'plant_name', 'plant_gln', 'location']
    template_name = "create.html"
    success_url = '/web/equipment/'

class EquipmentDelete(DeleteView):
    model = Equipment
    template_name = "equipment_confirm_delete.html"
    success_url = '/web/equipment/'