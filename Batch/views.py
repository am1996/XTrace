from django.shortcuts import render
from django.views.generic import *
from Batch.models import Batch
from SerialNumberPool.models import SerialNumberPool

class BatchIndex(ListView):
    model = Batch
    template_name = 'Batch/index.html'
    context_object_name = 'batches'

class BatchDetails(DetailView):
    model = Batch
    template_name = 'Batch/details.html'
    context_object_name = 'batch'

class BatchUpdate(UpdateView):
    model = Batch
    template_name = 'Batch/update.html'
    success_url = '/web/batches/'
    fields = ['batch_number', 'manufactured_at', 'expiry_date', 'quantity', 'sampled_quantity', 'order_number', 'batch_description']

class BatchCreate(CreateView):
    template_name = 'Batch/create.html'
    model = Batch
    success_url = '/web/batches/'
    fields = ['batch_number', 'product', 'manufactured_at', 'expiry_date', 'quantity', 'sampled_quantity', 'order_number', 'batch_description', 'serial_pool']

    def form_valid(self, form):
        serial_pool = SerialNumberPool.manager.create_pool_for_product(
            total_count=form.instance.quantity,
            user=self.request.user
        )
        return super().form_valid(form)

class BatchDelete(DeleteView):
    model = Batch
    template_name = 'Batch/batch_confirm_delete.html'
    success_url = '/web/batches/'