from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from Batch.models import Batch
from SerialNumberPool.models import SerialNumberPool

class BatchIndex(LoginRequiredMixin, ListView):
    model = Batch
    template_name = 'Batch/index.html'
    context_object_name = 'batches'

class BatchDetails(LoginRequiredMixin, DetailView):
    model = Batch
    template_name = 'Batch/details.html'
    context_object_name = 'batch'

class BatchUpdate(LoginRequiredMixin, UpdateView):
    model = Batch
    template_name = 'Batch/update.html'
    success_url = '/web/batch/'
    fields = ['batch_number', 'product', 'manufactured_at', 'expiry_date', 'quantity', 'sampled_quantity', 'order_number', 'batch_description', 'serial_pool']

class BatchCreate(LoginRequiredMixin, CreateView):
    template_name = 'Batch/create.html'
    model = Batch
    success_url = '/web/batch/'
    fields = ['batch_number', 'product', 'manufactured_at', 'expiry_date', 'quantity', 'sampled_quantity', 'order_number', 'batch_description', 'serial_pool']

class BatchDelete(LoginRequiredMixin, DeleteView):
    model = Batch
    template_name = 'Batch/batch_confirm_delete.html'
    success_url = '/web/batch/'