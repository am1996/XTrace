from typing import Any
from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from Equipment.models import Equipment
# Create your views here.

class EquipmentIndex(LoginRequiredMixin, ListView):
    model = Equipment
    template_name = "Equipment/index.html"
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["equipment_list"] = Equipment.objects.filter(deleted_at__isnull=True)
        return context
    
class EquipmentDetails(LoginRequiredMixin, DetailView):
    model = Equipment
    context_object_name = "equipment"
    template_name = "Equipment/details.html"

class EquipmentUpdate(LoginRequiredMixin, UpdateView):
    model = Equipment
    fields = ['name', 'model_number', 'serial_number', 'manufacturer', 'mac_address', 'ip_address', 'plant_name', 'plant_gln', 'location']
    template_name = "Equipment/update.html"
    success_url = '/web/equipment/' 

class EquipmentCreate(LoginRequiredMixin, CreateView):
    model = Equipment
    fields = ['name', 'model_number', 'serial_number', 'manufacturer', 'mac_address', 'ip_address', 'plant_name', 'plant_gln', 'location']
    template_name = "Equipment/create.html"
    success_url = '/web/equipment/'

class EquipmentDelete(LoginRequiredMixin, DeleteView):
    model = Equipment
    template_name = "Equipment/equipment_confirm_delete.html"
    success_url = '/web/equipment/'