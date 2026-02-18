from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import SerialNumberPool
from django.urls import reverse_lazy
# Create your views here.
# CRUD operations for SerialNumberPool To be implemented.

class SerialNumberPoolCreateView(LoginRequiredMixin, CreateView):
    model = SerialNumberPool
    template_name = 'SerialNumberPool/create.html'
    fields = ['total_to_generate', 'status']
    success_url = reverse_lazy('serialnumberpool:list')
    
    def form_valid(self, form):
        form.instance.generated_by = self.request.user
        return super().form_valid(form)

class SerialNumberPoolListView(LoginRequiredMixin, ListView):
    model = SerialNumberPool
    template_name = 'SerialNumberPool/list.html'
    context_object_name = 'serialnumberpools'

class SerialNumberPoolDetailView(LoginRequiredMixin, DetailView):
    model = SerialNumberPool
    template_name = 'SerialNumberPool/detail.html'
    context_object_name = 'serialnumberpool'

class SerialNumberPoolUpdateView(LoginRequiredMixin, UpdateView):
    model = SerialNumberPool
    template_name = 'SerialNumberPool/update.html'
    fields = ['total_to_generate', 'status']
    success_url = reverse_lazy('serialnumberpool:list')

class SerialNumberPoolDeleteView(LoginRequiredMixin, DeleteView):
    model = SerialNumberPool
    template_name = 'SerialNumberPool/serial_number_confirm_delete.html.html'
    success_url = reverse_lazy('serialnumberpool:list')