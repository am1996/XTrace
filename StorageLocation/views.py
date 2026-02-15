from typing import Any
from django.shortcuts import render
from django.views.generic import *

from StorageLocation.models import StorageLocation

# Create your views here.

# CRUD For StorageLocation

class StorageLocationIndex(ListView):
    model = StorageLocation
    template_name = "StorageLocation/index.html"
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["storage_location_list"] = StorageLocation.objects.all()
        return context

class StorageLocationDetails(DetailView):
    model = StorageLocation
    context_object_name = "storage_location"
    template_name = "StorageLocation/details.html"

class StorageLocationUpdate(UpdateView):
    model = StorageLocation
    fields = ['name', 'description']
    template_name = "StorageLocation/update.html"
    success_url = '/web/storage_location/'

class StorageLocationCreate(CreateView):
    model = StorageLocation
    fields = ['name', 'description']
    template_name = "StorageLocation/create.html"
    success_url = '/web/storage_location/'

class StorageLocationDelete(DeleteView):
    model = StorageLocation
    template_name = "StorageLocation/storage_location_confirm_delete.html"
    success_url = '/web/storage_location/'


