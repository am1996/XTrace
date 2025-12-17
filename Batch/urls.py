from django.contrib import admin
from django.urls import path
from Batch.views import *

app_name = "batch"

urlpatterns = [
    path('', BatchIndex.as_view(), name='batch_list'),
    path('create/', BatchCreate.as_view(), name='batch_create'),
]
