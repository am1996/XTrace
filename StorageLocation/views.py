from typing import Any
from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin

from StorageLocation.models import StorageLocation

# Create your views here.

# CRUD For StorageLocation

class StorageLocationIndex(LoginRequiredMixin, ListView):
    model = StorageLocation
    template_name = "StorageLocation/index.html"
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["storage_location_list"] = StorageLocation.objects.all()
        return context

class StorageLocationDetails(LoginRequiredMixin, DetailView):
    model = StorageLocation
    context_object_name = "storage_location"
    template_name = "StorageLocation/details.html"

class StorageLocationUpdate(LoginRequiredMixin, UpdateView):
    model = StorageLocation
    fields = ['name', 'gln', 'sub_location', 'location_type', 'address']
    template_name = "StorageLocation/update.html"
    success_url = '/web/storage_location/'

class StorageLocationCreate(LoginRequiredMixin, CreateView):
    model = StorageLocation
    fields = ['name', 'gln', 'sub_location', 'location_type', 'address']
    template_name = "StorageLocation/create.html"
    success_url = '/web/storage_location/'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class StorageLocationDelete(LoginRequiredMixin, DeleteView):
    model = StorageLocation
    template_name = "StorageLocation/storage_location_confirm_delete.html"
    success_url = '/web/storage_location/'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


