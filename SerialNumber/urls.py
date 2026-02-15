from django.contrib import admin
from django.urls import path
from .views import *

app_name = "serialnumber"
    
urlpatterns = [
    path('', SerialNumberListView.as_view(), name='serialnumber-list'),
    path('<int:pk>/', SerialNumberDetailView.as_view(), name='serialnumber_detail'),
    path('create/', SerialNumberCreateView.as_view(), name='serialnumber_create'),
    path('<int:pk>/update/', SerialNumberUpdateView.as_view(), name='serialnumber_update'),
    path('<int:pk>/delete/', SerialNumberDeleteView.as_view(), name='serialnumber_delete'),
]