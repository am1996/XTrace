from django.shortcuts import render
from django.views.generic import *
from .models import SerialNumberPool
from django.urls import reverse_lazy
# Create your views here.
# CRUD operations for SerialNumberPool To be implemented.

class SerialNumberPoolCreateView(CreateView):
    model = SerialNumberPool
    template_name = 'SerialNumberPool/create.html'
    fields = ['name', 'description', 'quantity']
    success_url = reverse_lazy('serialnumberpool:list')

class SerialNumberPoolListView(ListView):
    model = SerialNumberPool
    template_name = 'SerialNumberPool/list.html'
    context_object_name = 'serialnumberpools'

class SerialNumberPoolDetailView(DetailView):
    model = SerialNumberPool
    template_name = 'SerialNumberPool/detail.html'
    context_object_name = 'serialnumberpool'

class SerialNumberPoolUpdateView(UpdateView):
    model = SerialNumberPool
    template_name = 'SerialNumberPool/update.html'
    fields = ['name', 'description', 'quantity']
    success_url = reverse_lazy('serialnumberpool:list')

class SerialNumberPoolDeleteView(DeleteView):
    model = SerialNumberPool
    template_name = 'SerialNumberPool/serial_number_confirm_delete.html.html'
    success_url = reverse_lazy('serialnumberpool:list')