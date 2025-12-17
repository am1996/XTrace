from django.shortcuts import render
from django.views.generic import *
from Batch.models import Batch
from SerialNumberPool.models import SerialNumberPool
# Create your views here.

class BatchIndex(ListView):
    model = Batch
    template_name = 'index.html'
    context_object_name = 'batches'

class BatchDetails(DetailView):
    model = Batch
    template_name = 'details.html'
    context_object_name = 'batch'

class BatchUpdate(UpdateView):
    model = Batch
    template_name = 'update.html'
    success_url = '/batches/'
    fields = ['batch_number', 'manufactured_at', 'expiry_date', 'quantity', 'sampled_quantity', 'order_number', 'batch_description']

class BatchCreate(CreateView):
    template_name = 'create.html'
    model = Batch
    success_url = '/batches/'
    fields = ['batch_number', 'product', 'manufactured_at', 'expiry_date', 'quantity', 'sampled_quantity', 'order_number', 'batch_description']

    def form_valid(self, form):
        serial_pool = SerialNumberPool.manager.create_pool_for_product(
            total_count=form.instance.quantity,
            user=self.request.user
        )
        return super().form_valid(form)