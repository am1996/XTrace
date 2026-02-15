from django.contrib import admin
from django.urls import path
from .views import *

app_name = "storage_location"

urlpatterns = [
    path('', StorageLocationIndex.as_view(), name='storage_location_index'),
    path('<int:pk>/', StorageLocationDetails.as_view(), name='storage_location_details'),
    path('<int:pk>/edit', StorageLocationUpdate.as_view(), name='storage_location_update'),
    path('<int:pk>/delete', StorageLocationDelete.as_view(), name='storage_location_delete'),
    path('create/', StorageLocationCreate.as_view(), name='storage_location_create'),
]
