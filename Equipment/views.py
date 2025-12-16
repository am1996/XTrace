from django.shortcuts import render
from django.views.generic import *
from Equipment.models import Equipment
# Create your views here.

class EquipmentIndex(ListView):
    model = Equipment
    template_name = "index.html"
    