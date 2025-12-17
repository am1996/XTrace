from django.contrib import admin
from django.urls import path
from .views import *

app_name = "equipment"

urlpatterns = [
    path('', EquipmentIndex.as_view()),
    path('<int:pk>/', EquipmentDetails.as_view(), name='equipment_details'),
    path('<int:pk>/edit', EquipmentEdit.as_view(), name='equipment_update'),
    path('create/', EquipmentCreate.as_view(), name='equipment_create'),
]
