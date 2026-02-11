from django.contrib import admin
from django.urls import path
from .views import *

app_name = "user"

urlpatterns = [
    path('', UserIndex.as_view(), name='user_list'),
    path('<int:pk>/', UserDetails.as_view(), name='user_details'),
    path('<int:pk>/edit', UserUpdate.as_view(), name='user_update'),
    path('<int:pk>/delete', UserDelete.as_view(), name='user_delete'),
    path('create/', UserRegister.as_view(), name='user_create'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('logout/', UserLogout.as_view(), name='user_logout'),
]
