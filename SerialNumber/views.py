from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from SerialNumber.models import SerialNumber

# Create your views here.

# CRUD for serialnumbers

class SerialNumberListView(LoginRequiredMixin, ListView):
    model = SerialNumber
    template_name = 'SerialNumber/index.html'
    context_object_name = 'serialnumbers'

class SerialNumberDetailView(LoginRequiredMixin, DetailView):
    model = SerialNumber
    template_name = 'SerialNumber/details.html'
    context_object_name = 'serialnumber'

class SerialNumberCreateView(LoginRequiredMixin, CreateView):
    model = SerialNumber
    template_name = 'SerialNumber/create.html'
    fields = '__all__'
    success_url = '/web/serialnumber/'

class SerialNumberUpdateView(LoginRequiredMixin, UpdateView):
    model = SerialNumber
    template_name = 'SerialNumber/update.html'
    fields = '__all__'
    success_url = '/web/serialnumber/'

class SerialNumberDeleteView(LoginRequiredMixin, DeleteView):
    model = SerialNumber
    template_name = 'SerialNumber/serialnumber_confirm_delete.html'
    success_url = '/web/serialnumber/'