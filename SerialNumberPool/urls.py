from django.contrib import admin
from django.urls import path
from .views import *

app_name = "serialnumberpool"
    
urlpatterns = [
    path('', SerialNumberPoolListView.as_view(), name='list'),
    path('<int:pk>/', SerialNumberPoolDetailView.as_view(), name='detail'),
    path('<int:pk>/edit', SerialNumberPoolUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', SerialNumberPoolDeleteView.as_view(), name='delete'),
    path('create/', SerialNumberPoolCreateView.as_view(), name='create'),
]