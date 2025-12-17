from django.shortcuts import render
from django.views.generic import *
from Equipment.models import Equipment
# Create your views here.

class EquipmentIndex(ListView):
    model = Equipment
    context_object_name = "equipment_list"
    template_name = "index.html"
    
class EquipmentDetails(DetailView):
    model = Equipment
    context_object_name = "equipment"
    template_name = "equipment_details.html"

class EquipmentEdit(UpdateView):
    model = Equipment
    fields = ['name', 'description', 'serial_number', 'manufacturer', 'mac_address', 'ip_address', 'plant_name', 'plant_gln', 'location']
    template_name = "equipment_edit.html"
    success_url = '/web/equipment/' 

class EquipmentCreate(CreateView):
    model = Equipment
    fields = ['name', 'serial_number', 'manufacturer', 'mac_address', 'ip_address', 'plant_name', 'plant_gln', 'location']
    template_name = "create.html"
    success_url = '/web/equipment/'