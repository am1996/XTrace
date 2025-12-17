from django.contrib import admin
from django.urls import path
from .views import *

app_name = "equipment"

urlpatterns = [
    path('', EquipmentIndex.as_view(), name='equipment_list'),
    path('<int:pk>/', EquipmentDetails.as_view(), name='equipment_details'),
    path('<int:pk>/edit', EquipmentUpdate.as_view(), name='equipment_update'),
    path('<int:pk>/delete', EquipmentDelete.as_view(), name='equipment_delete'),
    path('create/', EquipmentCreate.as_view(), name='equipment_create'),
]
