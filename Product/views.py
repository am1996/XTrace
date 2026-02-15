from django.shortcuts import render
from django.views.generic import *
from Product.models import Product
# Create your views here.
# CRUD

class ProductListView(ListView):
    model = Product
    template_name = 'product/index.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/details.html'
    context_object_name = 'product'

class ProductCreateView(CreateView):
    model = Product
    template_name = 'product/create.html'
    fields = '__all__'
    success_url = '/web/products/'

class ProductUpdateView(UpdateView): 
    model = Product
    template_name = 'product/update.html'
    fields = '__all__'
    success_url = '/web/products/'

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/product_confirm_delete.html'
    success_url = '/web/products/'

