from django.shortcuts import render
from django.views.generic import *
from SerialNumber.models import SerialNumber

# Create your views here.

# CRUD for serialnumbers

class SerialNumberListView(ListView):
    model = SerialNumber
    template_name = 'serialnumber/index.html'
    context_object_name = 'serialnumbers'

class SerialNumberDetailView(DetailView):
    model = SerialNumber
    template_name = 'serialnumber/details.html'
    context_object_name = 'serialnumber'

class SerialNumberCreateView(CreateView):
    model = SerialNumber
    template_name = 'serialnumber/create.html'
    fields = '__all__'
    success_url = '/serialnumbers/'

class SerialNumberUpdateView(UpdateView):
    model = SerialNumber
    template_name = 'serialnumber/update.html'
    fields = '__all__'
    success_url = '/serialnumbers/'

class SerialNumberDeleteView(DeleteView):
    model = SerialNumber
    template_name = 'serialnumber/serialnumber_confirm_delete.html'
    success_url = '/serialnumbers/'