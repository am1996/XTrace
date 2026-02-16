from django.contrib import admin
from django.urls import path
from Batch.views import *

app_name = "batch"

urlpatterns = [
    path('', BatchIndex.as_view(), name='batch_list'),
    path('create/', BatchCreate.as_view(), name='batch_create'),
    path('<int:pk>/', BatchDetails.as_view(), name='batch_details'),
    path('<int:pk>/update/', BatchUpdate.as_view(), name='batch_update'),
    path('<int:pk>/delete/', BatchDelete.as_view(), name='batch_delete'),
]